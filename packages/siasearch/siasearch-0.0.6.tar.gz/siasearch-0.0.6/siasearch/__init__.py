from typing import Optional

from .siasearch import Siasearch
from .urls import DEVELOPMENT_SERVER


def auth(email: str, password: str, server: str = DEVELOPMENT_SERVER, viewer_server: Optional[str] = None):
    """Authorization function that returns the main interface to communicate with the SiaSearch platform

       Args:
           email: users email
           password: users password
           server: server to connect to
           viewer_server: optional server url to view results on

       Returns:
           Siasearch object. A Siasearch object allows you to run queries.
       Example:
           >>> # Create Sia object:
           >>> sia = auth("user@example.com", "password", "http://redfish-development.merantix.de")
           >>> # Use Sia object to run query, returning a `Results` object:
           >>> sia.query("dataset_name = 'kitti'")
    """

    return Siasearch(server, email, password, viewer_server)
