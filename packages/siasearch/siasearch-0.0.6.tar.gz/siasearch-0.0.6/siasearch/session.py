import io
import json
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import pandas as pd
import requests
from requests.utils import requote_uri


def _decode_parquet_buffer(content):
    buffer = io.BytesIO()
    buffer.write(content)
    return pd.read_parquet(buffer, engine="pyarrow")


class Session:
    """Session interface store server information and user auth token.
    It also have a number of useful helper for network managment for POST and GET http methods.
    And json/parquet desirialisation.
    SiaSearch uses Session to send query to the server
    as well as Segment us it for accesing GPS, Camera and metadata information.
    If you have local verstion of SiaSearch but want to have publicly sharable links to your cloud version,
    you might also pass `viewer_server` param.

    Examples:
        >>> sessions = Session("http://redfish-development.merantix.de", jwt_token="SOME_TOKEN")
        >>> sessions.get_json("/metrics_info")
        Returns list of metrics
    """

    def __init__(self, server: str, jwt_token: Optional[str] = None, viewer_server: Optional[str] = None):
        self.server = server
        self.jwt_token = jwt_token
        self.viewer_server = viewer_server if viewer_server else server

    def set_jwt_token(self, jwt_token: str):
        self.jwt_token = jwt_token

    def get(
        self, rel_url: str, params: Optional[Dict[str, Union[str, List[str]]]] = None, format: Optional[str] = None
    ):
        url = urljoin(self.server, rel_url)
        r = requests.get(requote_uri(url), params=params, headers={"Authorization": f"Bearer {self.jwt_token}"})
        if r.status_code == 500:
            raise RuntimeError(f"Server {self.server} encountered an error")
        if r.status_code != 200:
            raise RuntimeError(f"Server {self.server} returned status {r.status_code}. Response: {r.text}")
        if format:
            if format == "parquet":
                return _decode_parquet_buffer(r.content)
            elif format == "json_df":
                return pd.DataFrame.from_dict(json.loads(r.text))
            elif format == "json":
                return json.loads(r.text)
            else:
                raise ValueError(f"Unknown api format {format}")
        return r

    def post(self, rel_url, json_body: Dict, params: Optional[Dict] = None):
        url = urljoin(self.server, rel_url)
        r = requests.post(
            requote_uri(url), json=json_body, params=params, headers={"Authorization": f"Bearer {self.jwt_token}"}
        )
        if r.status_code != 200:
            raise RuntimeError(f"Server {self.server} returned status {r.status_code}. Response: {r.text}")
        return r

    def post_json(self, rel_url: str, params: Optional[Dict[str, str]]):
        return json.loads(self.post(rel_url, params).text)

    def get_json(self, rel_url: str, params: Optional[Dict[str, str]]) -> Any:
        return self.get(rel_url, params, "json")

    def __repr__(self):
        return f"<{self.__class__.__name__}(server={self.server}, viewer_server={self.viewer_server})>"
