# Defaults
DEVELOPMENT_SERVER = "https://redfish-development.merantix.de"

API_VERSION = 1

# Urls
API_BASE_URL = f"/public_api/v{API_VERSION}"
API_LOGIN_URL = f"{API_BASE_URL}/auth/login"
API_QUERY_URL = f"{API_BASE_URL}/segments"

METRICS_INFO_URL = f"{API_BASE_URL}/metrics_info"
SEGMENT_GPS_COORDINATES_URL = f"{API_BASE_URL}/drives/<drive_id>/gps/coordinates"
SEGMENT_CAMERA_SENSORS_NAMES_URL = f"{API_BASE_URL}/drives/<drive_id>/cameras/list"
SEGMENT_CAMERA_FRAMES_URL = f"{API_BASE_URL}/drives/<drive_id>/cameras/<camera_id>"
SEGMENT_METADATA_URL = f"{API_BASE_URL}/drives/<drive_id>/metadata"
GET_SEGMENT_TAGS_NAMES_URL = f"{API_BASE_URL}/drives/<drive_id>/tags/names"
ADD_SEGMENT_TAG_URL = f"{API_BASE_URL}/drives/<drive_id>/add_tag"
REMOVE_SEGMENT_TAG_URL = f"{API_BASE_URL}/drives/<drive_id>/remove_tag"
GET_TAGS_NAMES_URL = f"{API_BASE_URL}/tags/names"
GET_TAG_SEGMENTS_URL = f"{API_BASE_URL}/tags/segments"
REMOVE_TAGS_URL = f"{API_BASE_URL}/tags/remove"

# Complex Tags objects not supported by SDK yet
GET_TAGS_URL = f"{API_BASE_URL}/tags"
GET_SEGMENT_TAGS_URL = f"{API_BASE_URL}/drives/<drive_id>/tags"

# Query tags are not supported by SDK yet
GET_QUERY_TAGS_URL = f"{API_BASE_URL}/query/tags"
ADD_QUERY_TAG = f"{API_BASE_URL}/query/add_tag"
REMOVE_QUERY_TAG = f"{API_BASE_URL}/query/remove_tag"
