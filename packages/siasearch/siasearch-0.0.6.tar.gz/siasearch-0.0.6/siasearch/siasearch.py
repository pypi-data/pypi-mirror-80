from typing import Optional

import pandas as pd
import requests

from .results import Results
from .session import Session
from .urls import (
    API_LOGIN_URL,
    API_QUERY_URL,
    GET_TAG_SEGMENTS_URL,
    GET_TAGS_NAMES_URL,
    METRICS_INFO_URL,
    REMOVE_TAGS_URL,
)


class Siasearch:
    """Siasearch interface that maintains login credentials for backend connection and allows to query for drive
    segments of interest

     Examples:
         >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
         >>> sia
         'Siasearch object with user `user@example.com` connected to `http://redfish-development.merantix.de`'
         >>> sia.query("dataset_name = 'kitti_raw'")
         "Results for query `dataset_name = 'kitti_raw'`"
    """

    def __init__(self, server: str, email: str, password: str, viewer_server: Optional[str] = None):
        self.server = server.rstrip("/")
        self.email = email
        self._session = Session(server, viewer_server=viewer_server)
        self._session.set_jwt_token(self._login(self.email, password))

    def __str__(self):
        if self._session is None:
            return f"Connection to {self.server} was not established"
        return f"{self.__class__.__name__} object with user `{self.email}` connected to `{self.server}`"

    def __repr__(self):
        return self.__str__()

    def _login(self, email, password):
        try:
            data = {"email": email, "password": password}
            json_res = self._session.post_json(API_LOGIN_URL, data)
            return json_res["access_token"]
        except RuntimeError as e:
            print(f"Login failed: {e}")
            self._session = None

    def query(self, query: str) -> Results:
        """Query SiaSearch platform for segments

        Args:
            query: The query statements to execute

        Returns:
            `Results` object containing the results of the query

        Examples:
            >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
            >>> sia.query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'")
            "Results for query `dataset_name = 'kitti' AND curved_trajectory = 'RIGHT_BEND'`"

        """
        # TODO (timopheym): Preprocess query: enforce space before and after operator
        request_format = "parquet"
        params = {"query": query, "query_source": "python_api", "format": request_format}
        df_segments = self._session.get(API_QUERY_URL, params, request_format)
        return Results(self._session, df_segments, query=query)

    def get_metrics_info(self) -> pd.DataFrame:
        """Fetches information on all implemented metrics

        Returns:
            A pandas dataframe where the index corresponds to the metric name. The dataframe has the following
            columns:

            - type_value: The type of values for that particular metric. One of:
                - `range_double`
                - 'range_integer'
                - `ordinal`
                - `categorical`
                - `slider`
                - `map`

            - levels: For categorical and ordinal metrics shows the discrete values they can take

            - unit: Holds the unit of the metric if the metric has a unit e.g. m/s for `forward_velocity`

            - description: Description of the metric

            - display_name: Pretty-printable metric name

        Examples:
            >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
            >>> df = sia.get_metrics_info()
            >>> df.columns
            Index(['type_value', 'levels', 'unit', 'description', 'display_name'], dtype='object')
            >>> df.loc["curved_trajectory"].levels
            ["'LEFT_BEND'", "'NO_BEND'", "'RIGHT_BEND'"]
            >>> df.loc["curved_trajectory"].description
            'Categorical. `LEFT_BEND` / `RIGHT_BEND` for clips in which the vehicle trajectory monotonically changes
            its angle by at least 60 degrees. `NO_BEND` otherwise. '
            >>> df.loc["forward_velocity"].unit
            'm/s'

        """
        # TODO(robert): This dataframe is quite cluttered with all kinds of columns. Think of a way to
        #               allow the user to filter for specific types of columns that are relevant.
        df = self._session.get(METRICS_INFO_URL, format="json_df")
        df = df.set_index(["name"]).sort_index()
        df = df[["type_value", "levels", "unit", "description", "display_name"]]

        return df

    def get_all_tags(self):
        return self._session.get(GET_TAGS_NAMES_URL, None, "json")

    def get_results_from_tag(self, tag_name: str):
        request_format = "parquet"
        df_segments = self._session.get(GET_TAG_SEGMENTS_URL, {"tag_name": tag_name}, request_format)
        return Results(self._session, df_segments, tag=tag_name)

    def remove_tag(self, tag_name: str):
        try:
            self._session.post(REMOVE_TAGS_URL, {"tag_name": tag_name})
            print("Tag removed successfully")
        except requests.exceptions.RequestException:
            print("There was an error with removing tag")
