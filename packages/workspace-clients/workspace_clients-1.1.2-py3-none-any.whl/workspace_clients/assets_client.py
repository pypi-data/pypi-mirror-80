from marshmallow import EXCLUDE
from requests import Response
from clients_core.service_clients import E360ServiceClient
from typing import List, Any, Dict, Union
from .models import AssetType, AssetEmbed, AssetModel


class WorkspaceServiceAssetsClient(E360ServiceClient):
    """
    A client for the asset endpoint of workspace service
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid
        correlation_id (str): the correlation-id to be passed on the request headers

    """
    service_endpoint: str = ""
    extra_headers: Dict = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    def get_assets(self,
                   fields: List[str] = None,
                   type_: AssetType = None,
                   embed: List[AssetEmbed] = None,
                   metadata_key: str = "",
                   metadata_value: str = "",
                   sort: List[str] = None,
                   params: Dict = None,
                   **kwargs: Any) -> List[AssetModel]:
        """
        Creates a get request for the assets endpoint, returning the assets of the current user.
        By default all the assets will be returned without any pagination.

        Returns:
            list: a list of assets for the users that matched the provided filters

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """
        if not fields:
            fields = []
        if not embed:
            embed = []
        if not params:
            params = {}
        if not sort:
            sort = ["-created"]

        params["sort"] = ",".join(s for s in sort)
        if type_:
            params["type"] = type_.value
        if fields:
            params["fields"] = ",".join(fields)
        if embed:
            params["embed"] = ",".join(e.value for e in embed)
        if metadata_key:
            params["metadataKey"] = metadata_key
            params["metadataValue"] = metadata_value
        response = self.client.get("", params=params, headers=self.service_headers, raises=True, **kwargs)
        return self._response_to_model(response, many=True)  # type: ignore

    def delete(self, id_: str, **kwargs: AssetModel) -> bool:
        """
        Delete the specified asset, if it exists

        Returns:
            bool: True / False for successful / failed requests

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """
        response = self.client.delete(id_, headers=self.service_headers, raises=True, **kwargs)
        return response.ok

    def get_by_id(self, id_: str, **kwargs: Any) -> AssetModel:
        """
        Retrieve a single asset using its id

        Returns:
            AssetModel: The result asset matching the id provided

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """
        response = self.client.get(id_, headers=self.service_headers, raises=True, **kwargs)
        return self._response_to_model(response)  # type: ignore

    def post(self, asset: AssetModel, **kwargs: Any) -> AssetModel:
        """
        Create a new asset in workspaces

        Returns:
            AssetModel: The newly created asset, as returned by workspaces API

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """
        response = self.client.post('', json=AssetModel.Schema().dump(asset), headers=self.service_headers, raises=True, **kwargs)
        return self._response_to_model(response)  # type: ignore

    def patch_asset(self, id_: str, patch_document: List[Dict], **kwargs: Any) -> AssetModel:
        """
        Make changes to an existing asset. A JSON patch document needs to be passed to specify the changes that need to apply

        Returns:
            AssetModel: The updated asset, as returned by workspaces API

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """
        response = self.client.patch(id_, json=patch_document, raises=True, headers=self.service_headers, **kwargs)
        return self._response_to_model(response)  # type: ignore

    def _response_to_model(self, response: Response, many: bool = False) -> Union[List[AssetModel], AssetModel]:
        """
        Create AssetModel objects from response data, and inject an instance of current client
        to allow execution of methods directly from model objects

        Args:
            response: The response object as returned by the requests library
            many (Optional): Specifiy if we are expecting multiple or a single asset in the response. Defaults to False

        Returns:
            AssetModel: A list or a single AssetModel

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """
        response_json = response.json()["resources"] if many else [response.json()]
        result = AssetModel.Schema(many=True, unknown=EXCLUDE).load(response_json)
        for asset in result:
            asset.assets_client = self
        return result if many else result[0]
