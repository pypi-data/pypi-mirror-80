from typing import List, Optional

import pandas as pd

from .mixins import DisplaysUrl
from .segment import Segment
from .session import Session
from .utils import parse_query_url


class Results(DisplaysUrl):
    """Segments interface that holds multiple segments and allows a user to manipulate them in different ways

     Examples:
        >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
        >>> segments: Results = sia.query("dataset_name = 'kitti")
        >>> segments.df_segments()
    """

    _ordered_columns = ["drive_id", "start_timestamp", "end_timestamp", "dataset_name"]

    def __init__(
        self, session: Session, df_segments: pd.DataFrame, query: Optional[str] = None, tag: Optional[str] = None
    ):
        """Holds query results in the form of drive Segments.
           Only one origin of the data `query` or `tag` can be passed

        Args:
            df_segments:
            query: SiaSearch query associated with the data
            tag: Tag name associated with the data
        """
        if not tag and not query:
            raise Exception("One origin of segments, tag or query, should be presented!")

        if tag and query:
            raise Exception("Only one origin of segments, tag or query, can be presented!")

        self._query = query
        self._tag = tag
        self._df_segments = self._format_df_segments(df_segments)
        self._segments = None
        self._session = session

    def _format_df_segments(self, df):
        if df.shape[0] > 0:
            df = df[self._ordered_columns]
            df = df.sort_values(by="drive_id")
            df = df.reset_index(drop=True)

        return df

    @property
    def segments(self) -> List[Segment]:
        """Returns list of drive Segments corresponding to a query"""
        if self._segments is None:
            self._segments = [
                Segment(
                    self._session,
                    row.drive_id,
                    row.start_timestamp,
                    row.end_timestamp,
                    row.dataset_name,
                    query=self._query,
                    tag=self._tag,
                )
                for row in self._df_segments.itertuples()
            ]
        return self._segments

    @property
    def df_segments(self) -> pd.DataFrame:
        """Returns pd.DataFrame with Segments corresponding to a query

        Args:


        Returns:
          pandas DataFrame with segments
        """
        return self._df_segments

    def _get_url(self) -> Optional[str]:
        """Fetch string corresponding to the results of the query"""
        if self._query:
            query = parse_query_url(self._query)
            return f"{self._session.viewer_server}/search?query={query}&submit=true"
        return None

    def __repr__(self):
        content = ""

        if self._query:
            content = f"from query '{self._query}'"

        if self._tag:
            content = f"from tag '{self._tag}'"

        return f"<{self.__class__.__name__} class with {len(self._df_segments)} segments `{content}`)>"
