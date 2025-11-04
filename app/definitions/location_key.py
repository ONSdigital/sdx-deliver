from typing import TypedDict, Final


# Location Types
WINDOWS_SERVER: Final[str] = "windows_server"
GCS: Final[str] = "gcs"
S3: Final[str] = "s3"
CDP: Final[str] = "cdp"


class LocationKey(TypedDict):
    location_type: str
    location_name: str
