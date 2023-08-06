from clients_core.exceptions import ClientException
from marshmallow import Schema as Schema_
from typing import TYPE_CHECKING
from datetime import datetime
from typing import ClassVar, Type, Optional
from marshmallow_dataclass import dataclass as ma_dataclass
from dataclasses import field, InitVar
from enum import Enum


if TYPE_CHECKING:
    from .assets_client import WorkspaceServiceAssetsClient
    from .containers_client import WorkspaceServiceContainersClient


class LocationSearchType(Enum):
    SINGLE_LEVEL = "singleLevel"
    SUBTREE = "subtree"


class AssetType(Enum):
    ANALYTIC = "Analytic"
    ANALYTIC_DATASET = "Analytic Dataset"
    ANALYTIC_PACKAGE = "Analytic Package"
    ANALYTIC_WORKBENCH_PROJECT = "Analytics Workbench Project"
    CARD = "Card"
    COHORT = "Cohort"
    COHORT_PREVIEW = "Cohort Preview"
    CDM_9 = "Core Diabetes Model v9.0"
    CDM_9_5 = "Core Diabetes Model v9.5"
    COVARIATE_TEMPLATE = "Covariate Template"
    DATA_SLICE = "Data Slice"
    DESCRIPTIVE_ANALYTIC = "Descriptive Analytic"
    DOCUMENT = "Document"
    EVIDENCE_PLANNER_ASSET = "Evidence Planner Asset"
    EXPORT = "Export"
    GENOMIC_VARIANT_QUERY = "Genomic Variant Query"
    GROUPED_CODELIST = "Grouped Codelist"
    LINK = "Link"
    RECRUITMENT = "Recruitment"
    REPORT = "Report"
    VISUALIZATION = "Visualisation"


class ContainerEmbed(Enum):
    CHILDREN = "children"
    PARENT = "parent"
    SHARED_WITH = "sharedWith"


class AssetEmbed(Enum):
    PARENT = "parent"
    METADATA = "metadata"
    DATASET_INFO = "datasetInfo"


@ma_dataclass
class AssetModel:
    id: str
    type: str
    parent: Optional[dict] = None
    parent_id: Optional[str] = field(metadata=dict(data_key="parentAssetId"), default="")
    subtype: Optional[str] = None
    is_hidden: bool = field(metadata=dict(data_key="isHidden"), default=False)
    sent_by: Optional[str] = field(metadata=dict(data_key="sentByUserId"), default=None)
    dataset_info: Optional[dict] = field(metadata=dict(data_key="datasetInfo"), default=None)
    metadata: Optional[dict] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_favourite: Optional[bool] = field(metadata=dict(data_key="isFavourite"), default=None)
    rights: Optional[dict] = None
    created_by: Optional[str] = field(metadata=dict(data_key="createdByUserId"), default=None)
    is_shared: Optional[bool] = field(metadata=dict(data_key="isShared"), default=None)
    created: Optional[datetime] = field(default=None)
    updated: Optional[datetime] = field(default=None)
    Schema: ClassVar[Type[Schema_]] = Schema_  # needed for type checking
    assets_client: InitVar['WorkspaceServiceAssetsClient'] = None

    def __post_init__(self, assets_client: 'WorkspaceServiceAssetsClient ' = None) -> None:
        self.assets_client = assets_client

    def delete(self) -> bool:
        if self.assets_client is None:  # type: ignore
            message = (
                "Can not perform AssetMode.delete operation."
                "No instance of WorkspaceServiceAssetsClient has been provided to this model."
                "Please use WorkspaceServiceAssetsClient.delete function instead")

            raise ClientException(message)
        return self.assets_client.delete(self.id)  # type: ignore


@ma_dataclass
class ContainerModel:
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = "standard"
    description: Optional[str] = None
    parent: Optional[dict] = None
    shared_with: Optional[dict] = field(metadata=dict(data_key="sharedWith"), default=None)
    children: Optional[dict] = None
    rights: Optional[dict] = None
    created: Optional[datetime] = field(default=None)
    updated: Optional[datetime] = field(default=None)
    Schema: ClassVar[Type[Schema_]] = Schema_  # needed for type checking
    total_descendant_asset_count: Optional[int] = field(default=None, metadata=dict(data_key="totalDescendantAssets"))
    containers_client: InitVar['WorkspaceServiceContainersClient'] = None

    def __post_init__(self, containers_client: 'WorkspaceServiceContainersClient' = None) -> None:
        self.containers_client = containers_client

    def delete(self) -> bool:
        if self.containers_client is None:  # type: ignore
            message = (
                "Can not perform ContainerModel.delete operation. "
                "No instance of WorkspaceServiceContainersClient has been provided to this model."
                "Please use WorkspaceServiceContainersClient.delete function instead")
            raise ClientException(message)
        return self.containers_client.delete(self.id)  # type: ignore
