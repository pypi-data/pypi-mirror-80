import json
from typing import Callable, List, Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
import requests
from skimage import io

from .session import Session
from .mixins import DisplaysUrl
from .urls import (
    ADD_SEGMENT_TAG_URL,
    GET_SEGMENT_TAGS_NAMES_URL,
    REMOVE_SEGMENT_TAG_URL,
    SEGMENT_CAMERA_FRAMES_URL,
    SEGMENT_CAMERA_SENSORS_NAMES_URL,
    SEGMENT_GPS_COORDINATES_URL,
    SEGMENT_METADATA_URL,
)
from .utils import parse_query_url

TIME_STRING_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEFAULT_CAMERA = "camera_00"


class Segment(DisplaysUrl):
    """A Segment corresponds to an individual query result, specified by drive_id, start_timestamp, and end_timestamp.
    The Segment class wraps all information on the query result and provides utility methods to access that data.
    """

    def __init__(
        self,
        session: Session,
        drive_id: str,
        start_timestamp: pd.Timestamp,
        end_timestamp: pd.Timestamp,
        dataset_name: Optional[str] = None,
        query: Optional[str] = None,
        tag: Optional[str] = None,
    ):
        self._session = session
        self._drive_id = drive_id
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self._dataset_name = dataset_name
        self._query = query
        self._tag = tag

        self._gps_coordinates = None
        self._camera_sensors_names = None
        self._camera_sensors = {}

    def __repr__(self):
        content = f"drive_id='{self._drive_id}', start_timestamp='{self._start_timestamp}', "
        f"end_timestamp='{self._end_timestamp}'"

        if self._dataset_name:
            content = f"{content}, dataset_name='{self._dataset_name}'"

        if self._query:
            content = f"{content}, query='{self._query}'"

        if self._tag:
            content = f"{content}, tag='{self._tag}'"

        return f"<{self.__class__.__name__}({content})>"

    def _get_drive_url(self, url):
        return url.replace("<drive_id>", self._drive_id)

    def _get_timestamps_as_url_params(self):
        return {
            "start_timestamp": self._start_timestamp.strftime(TIME_STRING_FORMAT),
            "end_timestamp": self._end_timestamp.strftime(TIME_STRING_FORMAT),
        }

    def get_gps(self) -> pd.DataFrame:
        """Get the GPS coordinates for a Segment

        Returns:
            A dataframe of GPS coordinates. The dataframe has the columns `drive_id`, `latitude` and `longitude` with
            the index holding the corresponding timestamps.

        Examples:
            >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
            >>> seg = sia.query("dataset_name = 'kitti_raw'").segments[0]
            >>> seg.get_gps().head(3)
                                                                drive_id   latitude  longitude
            timestamp
            2011-09-26 13:02:25.964389+00:00  2011_09_26_drive_0001_sync  49.015004   8.434297
            2011-09-26 13:02:26.074348+00:00  2011_09_26_drive_0001_sync  49.014997   8.434280
            2011-09-26 13:02:26.174598+00:00  2011_09_26_drive_0001_sync  49.014991   8.434265
        """
        if self._gps_coordinates is None:
            url = self._get_drive_url(SEGMENT_GPS_COORDINATES_URL)
            self._gps_coordinates = self._session.get(url, self._get_timestamps_as_url_params(), "parquet")
        return self._gps_coordinates

    def available_cameras(self) -> List[str]:
        """Get list of available cameras for a Segment

        Returns:
            List of available camera names

        Examples:
            >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
            >>> seg = sia.query("dataset_name = 'kitti_raw'").segments[0]
            >>> seg.available_camers()
            ['camera_00', 'camera_01', 'camera_02', 'camera_03']
        """
        if self._camera_sensors_names is None:
            url = self._get_drive_url(SEGMENT_CAMERA_SENSORS_NAMES_URL)
            self._camera_sensors_names = self._session.get_json(url, {})
        return self._camera_sensors_names

    def get_image_paths(self, camera_id: str = DEFAULT_CAMERA) -> pd.Series:
        """Get references to camera data for a Segment

        Args:
            camera_id: Specifies data from which camera to get. To see available cameras use `available_cameras`.

        Returns:
            A Series where the values are references to camera frames and the index is the corresponding timestamp

        Examples:
            >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
            >>> seg = sia.query("dataset_name = 'kitti_raw'").segments[0]
            >>> seg.get_image_paths("camera_00").head(3)
            timestamp
            2011-09-26 13:02:26.064785+00:00    https://storage.googleapis.com/mx-automotive-d...
            2011-09-26 13:02:26.167923+00:00    https://storage.googleapis.com/mx-automotive-d...
            2011-09-26 13:02:26.270924+00:00    https://storage.googleapis.com/mx-automotive-d...
            Name: image_fpath, dtype: object
        """
        if camera_id not in self._camera_sensors:
            url = self._get_drive_url(SEGMENT_CAMERA_FRAMES_URL).replace("<camera_id>", camera_id)
            camera = self._session.get(url, self._get_timestamps_as_url_params(), "parquet")
            if isinstance(camera, pd.DataFrame):
                assert camera.shape[1] == 1, "Expected a single column to transform DataFrame to Series"
            self._camera_sensors[camera_id] = camera.iloc[:, 0]
        return self._camera_sensors[camera_id]

    def get_raw_values(self, metrics: Union[List[str], str]) -> pd.DataFrame:
        """Get raw values from the specified columns for a Segment

        Args:
            metrics: list of the raw value columns to fetch

        Returns:
            A dataframe containing all the data for the columns specified and their corresponding timestamps as the
            index

        Examples:
            >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
            >>> seg = sia.query("dataset_name = 'kitti_raw'").segments[0]
            >>> seg.get_raw_values(["forward_velocity", "forward_acceleration"]).head(3)
                                     forward_velocity  forward_acceleration
            timestamp
            2011-09-26 13:02:26.000         13.172717             -0.340301
            2011-09-26 13:02:26.100         13.129880             -0.447682
            2011-09-26 13:02:26.200         13.084994             -0.440583
        """
        if isinstance(metrics, str):
            metrics = [metrics]
        url = self._get_drive_url(SEGMENT_METADATA_URL)
        params = self._get_timestamps_as_url_params()
        params["metrics"] = json.dumps(metrics)
        df = self._session.get(url, params, "parquet")
        return df

    def _get_url(self) -> str:
        """Get the URL corresponding to the segment"""
        query_url = f"start_timestamp={self._start_timestamp.strftime(TIME_STRING_FORMAT)}&"
        f"end_timestamp={self._end_timestamp.strftime(TIME_STRING_FORMAT)}"
        if self._query:
            query_url = f"{query_url}&query={self._query}"

        query_url = parse_query_url(query_url)
        return f"{self._session.viewer_server}/drives/{self._drive_id}?{query_url}"

    def preview_images(
        self, load_image: Callable = io.imread, camera_id: str = DEFAULT_CAMERA, num_rows: int = 3, num_columns: int = 2
    ) -> None:
        """Shows a grid of equally spaced (in time) images from a Segment

        Shows `num_rows * num_columns` images as a matplotlib figure

        Args:
            load_image: A function that can open images using paths provided by `self.get_image_paths`
            camera_id: The camera to preview images from
            num_rows: Number of rows for the image grid
            num_columns: Number of columns for the image grid
        """
        fig, ax = plt.subplots(num_rows, num_columns)
        camera_series = self.get_image_paths(camera_id)
        step_size = len(camera_series) // (num_rows * num_columns)
        counter = 0
        first_ts = camera_series.index[0]
        for i in range(num_rows):
            for j in range(num_columns):
                ts, img_path = camera_series.index[counter * step_size], camera_series.iloc[counter * step_size]
                img = load_image(img_path)
                ax[i, j].imshow(img)
                ax[i, j].set_title(ts - first_ts)
                ax[i, j].set_axis_off()
                counter += 1

    def get_tags(self):
        return self._session.get(
            self._get_drive_url(GET_SEGMENT_TAGS_NAMES_URL), self._get_timestamps_as_url_params(), "json"
        )

    def add_tag(self, tag_name):
        try:
            self._session.post(
                self._get_drive_url(ADD_SEGMENT_TAG_URL),
                {"tag_name": tag_name, "query_str": self._query, **self._get_timestamps_as_url_params()},
            )
            print("Tag added successfully")
        except requests.exceptions.RequestException:
            print("There was an error with adding tag")

    def remove_tag(self, tag_name):
        try:
            self._session.post(
                self._get_drive_url(REMOVE_SEGMENT_TAG_URL),
                {"tag_name": tag_name, **self._get_timestamps_as_url_params()},
            )
            print("Tag removed successfully")
        except requests.exceptions.RequestException:
            print("There was an error with removing tag")
