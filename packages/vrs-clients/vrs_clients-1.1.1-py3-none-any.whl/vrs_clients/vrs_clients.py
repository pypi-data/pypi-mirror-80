import pathlib
from typing import Dict, Any
from marshmallow import EXCLUDE
from clients_core.service_clients import E360ServiceClient
from .models import PlotlyVisualisationModel, VisualisationModel
from .utils import VRSConverter


class PlotlyVisualizationResourceClient(E360ServiceClient):
    """
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid

    """
    service_endpoint = ""
    extra_headers = {
        "accept": "application/json",
        "Content-Type": "application/json-patch+json"
    }

    def create(self, payload: Dict, from_plotly: bool = False, **kwargs: Any) -> PlotlyVisualisationModel:
        """
        Creates a visualisation, returns a deserialised model instance.

        Args:
            from_plotly: converts from a plotly payload to a VRS payload structure, default False
            payload: VRS compatible plotly payload
            from_plotly: if True, will convert a plotly payload to a VRS payload

        """
        if from_plotly is True:
            data = VRSConverter(payload).dump()
        else:
            data = PlotlyVisualisationModel.Schema().dump(payload)  # type: ignore

        response = self.client.post('', json=data, headers=self.service_headers, raises=True, **kwargs)

        response_json = response.json()
        return PlotlyVisualisationModel.Schema(unknown=EXCLUDE).load(response_json)  # type: ignore

    def delete_by_id(self, visualisation_id: str, **kwargs: Any) -> bool:
        """
        Delete the visualisation object by its id. Returns True when deleted successfully.
        """
        response = self.client.delete(visualisation_id, headers=self.service_headers, **kwargs)
        return response.ok


class VisualizationResourceClient(E360ServiceClient):
    """
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid

    """
    service_endpoint = ""
    extra_headers = {
        "accept": "application/json",
        "Content-Type": "application/json-patch+json"
    }

    def create(self, payload: Dict, **kwargs: Any) -> VisualisationModel:
        """
        Creates a visualisation, returns a deserialised model instance.

        Args:
            payload: VRS compatible visualisation payload

        """
        data = VisualisationModel.Schema().dump(payload)  # type: ignore
        response = self.client.post('', json=data, headers=self.service_headers, raises=True, **kwargs)

        response_json = response.json()
        return VisualisationModel.Schema(unknown=EXCLUDE).load(response_json)  # type: ignore

    def delete_by_id(self, visualisation_id: str, **kwargs: Any) -> bool:
        """
        Delete the visualisation object by its id. Returns True when deleted successfully.
        """
        response = self.client.delete(visualisation_id, headers=self.service_headers, **kwargs)
        return response.ok

    def upload_file(self, visualisation_id: str, file_path: pathlib.Path, **kwargs: Any) -> bool:
        """
        Upload a file for an existing visualisation.

        Args:
            visualisation_id: id of an existing visualisation
            file_path: file path object which needs to be uploaded

        Kwargs:
            timeout (int): optional, maximum value in seconds for the operation to run for.

        """
        with file_path.open('rb') as file_buffer:
            response = self.client.put(
                f'{visualisation_id}/data',
                data=file_buffer,
                headers=self.service_headers,
                raises=True,
                **kwargs)
        return response.ok

    def create_and_upload(self, payload: Dict, file_path: pathlib.Path, **kwargs: Any) -> VisualisationModel:
        """
        Combines creation of a visualisation and uploading of the file.
        """
        visualisation = self.create(payload, **kwargs)
        self.upload_file(visualisation.id, file_path, **kwargs)
        return visualisation
