from functools import reduce
import warnings
from typing import List, Union, Callable, Optional, TypeVar, Type, Dict, Any
from dataclasses import asdict
import logging
from pathlib import Path
from uuid import uuid4

from clients_core.authentication.token_handler import OIDCTokenHandler, TokenHandler
from clients_core.rest_client import RestClient
from clients_core.secured_rest_client import SecuredRestClient
from clients_core.authentication.cache import DictCache
from clients_core.authentication.token_cache import TokenCache
from clients_core.api_match_client import ServiceDirectoryMatchClient, MatchSpec, GatewayMatchClient, ApiMatchClient
from adt_clients import AnalyticDatasetClient, AnalyticDatasetDefinitionClient
from adt_clients.models import AnalyticDatasetModel, Granularity, AnalyticDatasetFormat
from workspace_clients import WorkspaceServiceAssetsClient, WorkspaceServiceContainersClient
from workspace_clients.models import AssetType, ContainerModel, AssetModel, AssetEmbed
from sd_clients import ServiceDirectoryClient, ApiGatewayProvider
from file_service_client import FileServiceClient
from vrs_clients import PlotlyVisualizationResourceClient, VisualizationResourceClient

from iqvia_e360 import Settings
from iqvia_e360.exceptions import ClientWrapperError
from iqvia_e360.models import AdtReportAssetModel, ContainerAssetModel, ClientStoreAssetModel


logger = logging.getLogger(__name__)
ADT_OUTPUT_TYPE = "AnalyticDataset/OutputType"
ADT_TYPES = {
    "CSV": ("csv", "text/csv"),
    "PARQUET": ("parquet", "application/vnd.apache.parquet"),
    "ZIP": ("zip", "application/zip")
}

T = TypeVar("T")


class ClientStore:
    _api_gateway_key: Optional[str] = None
    _oidc_user_id: Optional[str] = None
    _token_cache: Optional[TokenHandler] = None
    _verify_ssl: bool = True
    _match_client: ApiMatchClient
    _adt_rest_client: AnalyticDatasetClient
    _adt_definition_rest_client: AnalyticDatasetDefinitionClient
    _ws_asset_rest_client: WorkspaceServiceAssetsClient
    _ws_container_rest_client: WorkspaceServiceContainersClient
    _fs_rest_client: FileServiceClient
    _vrs_plotly_rest_client: PlotlyVisualizationResourceClient
    _vrs_rest_client: VisualizationResourceClient

    def __init__(self, match_client: ApiMatchClient, api_gateway_key: str = None,
                 token_cache: TokenHandler = None, oidc_user_id: str = None, verify_ssl: bool = True):
        if not api_gateway_key and not token_cache:
            raise ValueError("api_gateway_key or token_cache must be provided for initialization")
        if api_gateway_key and token_cache:
            raise ValueError("api_gateway_key and token_cache provided. Please only provide the authentication method wished to be used.")
        self._match_client = match_client
        self._api_gateway_key = api_gateway_key
        self._token_cache = token_cache
        self._oidc_user_id = oidc_user_id
        self._verify_ssl = verify_ssl
        if token_cache and not oidc_user_id:
            warnings.warn('OIDC authentication set-up, but no `oidc_user_id` provided. Some features may not work as expected.')

    @classmethod
    def create_from_settings(cls, settings_path: Union[Path, str] = Settings.settings_path) -> 'ClientStore':
        f"""Initialze The client store using a settings file. This will be under the default location {Settings.settings_path}
        or it can be on a custom location specified as an argument.

        Args:
            settings_path: The path to the settings file

        Returns:
            New ClientStore instance

        """
        if not isinstance(settings_path, Path):
            settings_path = Path(settings_path)
        settings = Settings(settings_path=settings_path)
        if settings.is_api_gateway_mode:
            return cls.create_with_gateway(settings.api_gateway_key, settings.api_gateway_url, settings.verify_ssl)  # type: ignore
        elif settings.is_oidc_mode:
            return cls.create_with_oidc(settings.service_directory_url,  # type: ignore
                                        settings.oidc_endpoint_url, settings.oidc_client_id,  # type: ignore
                                        settings.oidc_client_secret, settings.oidc_user_id, settings.verify_ssl)  # type: ignore
        else:
            raise ClientWrapperError("Improperly configured, no valid OIDC or Api-Gateway settings")

    @classmethod
    def create_with_gateway(cls, api_key: str, gateway_url: str = Settings.api_gateway_url, verify_ssl: bool = True) -> 'ClientStore':
        provider = ApiGatewayProvider(gateway_url)
        match_client = GatewayMatchClient(provider)
        return ClientStore(match_client, api_key, None, None, verify_ssl)

    @classmethod
    def create_with_oidc(cls,
                         service_directory_url: str,
                         oidc_endpoint: str,
                         client_id: str,
                         client_secret: str,
                         oidc_user_id: str = None,
                         verify_ssl: bool = True,
                         token_cache_callback: Callable = None) -> 'ClientStore':
        token_handler = OIDCTokenHandler(f"{oidc_endpoint.rstrip('/')}/connect/token", client_id, client_secret, verify_ssl)
        token_cache = token_cache_callback(token_handler) if token_cache_callback else TokenCache(DictCache(), token_handler)
        rest_client = SecuredRestClient(service_directory_url, ["service-directory-service"], token_cache, verify_ssl=verify_ssl)
        sd_client = ServiceDirectoryClient(rest_client)
        match_client = ServiceDirectoryMatchClient(sd_client)
        return ClientStore(match_client, None, token_cache, oidc_user_id, verify_ssl)

    @property
    def is_api_gateway_mode(self) -> bool:
        return bool(self._api_gateway_key) and not bool(self._token_cache)

    def get_rest_client(self, match_spec: MatchSpec) -> RestClient:
        if self.is_api_gateway_mode:
            return self._match_client.get_simple_client(match_spec, extra_params={"apiKey": self._api_gateway_key}, verify_ssl=self._verify_ssl)
        else:
            return self._match_client.get_secured_client(
                match_spec, self._token_cache, verify_ssl=self._verify_ssl)

    def _get_service_client(self, match_spec: MatchSpec,
                            ServiceClass: Type[T],
                            attr: str, user_id: str = None) -> T:
        if not user_id:
            user_id = self._oidc_user_id
        if not hasattr(self, attr):
            setattr(self, attr, self.get_rest_client(match_spec))
        return ServiceClass(getattr(self, attr), user_id=user_id)  # type: ignore

    def get_vrs_plotly_client(self, user_id: str = None) -> PlotlyVisualizationResourceClient:
        match_spec = MatchSpec(
            "visualization-resource-service",
            "Plotly", 1, 0, 0,
            ["visualizations-service"])
        return self._get_service_client(match_spec, PlotlyVisualizationResourceClient, "_vrs_plotly_rest_client", user_id)

    def get_vrs_client(self, user_id: str = None) -> PlotlyVisualizationResourceClient:
        match_spec = MatchSpec(
            "visualization-resource-service",
            "Visualizations", 1, 0, 0,
            ["visualizations-service"])
        return self._get_service_client(match_spec, VisualizationResourceClient, "_vrs_rest_client", user_id)

    def get_workspace_asset_client(self, user_id: str = None) -> WorkspaceServiceAssetsClient:
        match_spec = MatchSpec(
            "E360-Workspace-Service",
            "AssetService", 3, 0, 0,
            ["e360_workspace_service"])
        return self._get_service_client(match_spec, WorkspaceServiceAssetsClient, "_ws_asset_rest_client", user_id)

    def get_workspace_container_client(self, user_id: str = None) -> WorkspaceServiceContainersClient:
        match_spec = MatchSpec(
            "E360-Workspace-Service",
            "ContainerService", 2, 0, 0,
            ["e360_workspace_service"])

        return self._get_service_client(match_spec, WorkspaceServiceContainersClient, "_ws_container_rest_clien", user_id)

    def get_fs_client(self, user_id: str = None) -> FileServiceClient:
        match_spec = MatchSpec(
            "E360-File-Service",
            "Files", 1, 0, 0,
            ["file-service"])

        return self._get_service_client(match_spec, FileServiceClient, "_fs_rest_client", user_id)

    def get_adt_definition_client(self, user_id: str = None) -> AnalyticDatasetDefinitionClient:
        match_spec = MatchSpec(
            "E360-AnalyticDatasetTools-Service",
            "AnalyticDatasetDefinition", 1, 0, 0,
            ["e360_analytic_dataset_tools_service"])

        return self._get_service_client(match_spec, AnalyticDatasetDefinitionClient, "_adt_definition_rest_client", user_id)

    def get_adt_client(self, user_id: str = None) -> AnalyticDatasetClient:
        match_spec = MatchSpec(
            "E360-AnalyticDatasetTools-Service",
            "AnalyticDataset", 1, 0, 0,
            ["e360_analytic_dataset_tools_service"])

        return self._get_service_client(match_spec, AnalyticDatasetClient, "_adt_rest_client", user_id)

    def get_adt_reports(self, metadata_key: str = None, metadata_value: str = None) -> List[AdtReportAssetModel]:
        ws_client = self.get_workspace_asset_client()
        params = {"subtype": "Report", "embed": "metadata"}
        if metadata_key and metadata_value:
            params["metadataKey"] = metadata_key
            params["metadataValue"] = metadata_value
        elif metadata_key or metadata_value:
            raise ValueError("metadata_key or metadata_value provided. Please provide both values for filtering")
        assets = ws_client.get_assets(type_=AssetType.ANALYTIC_DATASET, params=params)
        # Some corrupted assets are missing LocalAssetId and can't be used for downloads
        downloadable_assets = [asset for asset in assets if asset.metadata and "LocalAssetId" in asset.metadata]
        return [AdtReportAssetModel(client_store=self, **asdict(i)) for i in downloadable_assets]

    def get_adt_report_by_id(self, id_: str) -> AdtReportAssetModel:
        reports = self.get_adt_reports(metadata_key="LocalAssetId", metadata_value=id_)
        if not reports:
            raise ClientWrapperError(f"No assets found for Analytic Dataset Report: {id_}")
        return reports[0]

    def get_workspace_containers(self, name: str = None) -> List[ContainerAssetModel]:
        ws_client = self.get_workspace_container_client()
        containers = ws_client.get(name=name)
        return [ContainerAssetModel(containers_client=ws_client, client_store=self, **asdict(i)) for i in containers]

    def move_workspace_asset(self, asset: Union[str, AssetModel],
                             target_container: Union[ContainerModel, str],
                             new_name: str = None, hidden: bool = False) -> AssetModel:
        ws_client = self.get_workspace_asset_client()
        if isinstance(asset, AssetModel):
            asset = asset.id
        if isinstance(target_container, ContainerModel):
            target_container = target_container.id
        payload = [
            {"value": target_container, "path": "/parent/id", "op": "replace"},
            {"value": hidden, "path": "/isHidden", "op": "replace"},
        ]
        if new_name:
            payload.append({"value": new_name, "path": "/name", "op": "replace"})

        return ws_client.patch_asset(asset, payload)

    def create_workspace_container(self, target_container: Union[ContainerModel, str], name: str, description: str = "") -> ContainerAssetModel:
        if isinstance(target_container, ContainerModel):
            target_container = target_container.id
        ws_client = self.get_workspace_container_client()
        new_container = ws_client.post(ContainerModel(name=name, parent={"id": target_container}, description=description))
        return ContainerAssetModel(containers_client=ws_client, client_store=self, **asdict(new_container))

    def download_adt_report(self, asset: Union[AdtReportAssetModel, str], location: str = None) -> Optional[Path]:
        if isinstance(asset, str):
            ws_client = self.get_workspace_asset_client()
            asset_model = ws_client.get_by_id(asset)
        else:
            asset_model = asset
        report_id = asset_model.metadata["LocalAssetId"]
        adt_type = ADT_TYPES[asset_model.metadata[ADT_OUTPUT_TYPE]]
        if location is None:
            replace_pairs = [(" ", "_"), ("/", "_")]
            path = reduce(lambda acc, it: acc.replace(*it), replace_pairs, asset_model.name)
            location_path = Path(f"{path}.{adt_type[0]}")
        else:
            location_path = Path(location)
        return self.download_adt_report_by_id(report_id, location_path, adt_type[1])

    def download_adt_report_by_id(self, report_id: str, location: Path, content_type: str) -> Optional[Path]:
        adt_client = self.get_adt_client()
        ok = adt_client.download_report(report_id, location, content_type)
        return location if ok else None

    def create_workspace_asset(self, asset: AssetModel) -> AssetModel:
        ws_client = self.get_workspace_asset_client()
        return ws_client.post(asset)

    def upload_document_file(self, target_container: Union[ContainerModel, str], file_path: str, name: str, description: str = "") -> Optional[AssetModel]:
        if isinstance(target_container, ContainerModel):
            target_container = target_container.id
        fs_client = self.get_fs_client()
        upload = fs_client.create(Path(file_path))
        metadata = {
            "Document/FilePath": Path(file_path).name,
            "Document/FileId": upload["id"]
        }
        asset = AssetModel(
            is_hidden=False,
            id=upload["id"],
            parent={"id": target_container},
            name=name,
            description=description,
            type=AssetType.DOCUMENT.value, metadata=metadata)
        try:
            return self.create_workspace_asset(asset)
        except Exception:
            fs_client.delete_by_id(upload["id"])
            return None

    def upload_adt_file(self, target_container: Union[ContainerModel, str], file_path: str, name: str, granularity: Granularity, format_: AnalyticDatasetFormat, dataset_release_id: str = None) -> AnalyticDatasetModel:
        adt_client = self.get_adt_client()
        definition_client = self.get_adt_definition_client()
        upload = adt_client.upload_file(Path(file_path), granularity, format_, dataset_release_id=dataset_release_id)
        definition = definition_client.get(upload.definition_id)
        self.move_workspace_asset(definition.asset_id, target_container, name)
        self.move_workspace_asset(upload.asset_id, target_container, name)
        return upload

    def create_plotly_visualization(self, plotly_obj: Dict, target_container: Union[ContainerModel, str], name: str, description: str = "") -> AssetModel:
        if isinstance(target_container, ContainerModel):
            target_container = target_container.id
        vrs_client = self.get_vrs_plotly_client()
        vrs_object = vrs_client.create(plotly_obj, from_plotly=True)
        asset = AssetModel(
            id=str(uuid4()),
            parent={"id": target_container},
            name=name,
            description=description,
            type=AssetType.VISUALIZATION.value,
            metadata={
                "LocalAssetId": vrs_object.id,
                "VisType": "Plotly"
            })
        return self.create_workspace_asset(asset)

    def get_assets(self, *args: Any, user_id: str = None, **kwargs: Any) -> List[AssetModel]:
        ws_client = self.get_workspace_asset_client(user_id)
        embed = kwargs.get("embed", [])
        embed.append(AssetEmbed.METADATA)
        kwargs["embed"] = embed
        assets = ws_client.get_assets(*args, **kwargs)
        return [ClientStoreAssetModel.create(asset, self) for asset in assets]
