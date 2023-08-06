from typing import Dict, Any
from clients_core.service_clients import E360ServiceClient
from clients_core.exceptions import ClientValueError


class ChartImageServicePlotlyClient(E360ServiceClient):
    """
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid

    """
    service_endpoint = "image"
    extra_headers = {"accept": "application/octet-stream"}
    PNG_MAGIC = b'\x89\x50\x4e\x47'

    def get_chart_bytes(self, data: Dict, **kwargs: Any) -> bytes:
        """
        Requests for a chart PNG image to be created from a Plotly payload.

        Args:
            data (dict): Plotly payload of the chart
            **kwargs: passed onto the rest client's request

        Returns:
            bytes: image as a binary string

        Raises:
            ClientValueError: when things don't go as expected.

        """
        response = self.client.post(self.service_endpoint, json=data, headers=self.get_ims_claims(), **kwargs)
        if not response.ok:
            raise ClientValueError(f'Error getting a chart data. {response}: {response.text}')
        elif not response.content:
            raise ClientValueError('Charting endpoint returned an empty response')
        elif not response.content.startswith(self.PNG_MAGIC):
            raise ClientValueError(f"Bad chart data received: {response.content[:100]}")
        return response.content
