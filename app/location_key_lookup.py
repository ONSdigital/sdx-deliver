from typing import Final

from app.definitions import LocationKeyLookupBase, LocationKey
from app.definitions import LocationNameRepositoryBase, LookupKey

# Location Types
WINDOWS_SERVER: Final[str] = "windows_server"
GCS: Final[str] = "gcs"
S3: Final[str] = "s3"
CDP: Final[str] = "cdp"


class LocationKeyLookup(LocationKeyLookupBase):

    def __init__(self, location_name_repo: LocationNameRepositoryBase):
        self._location_name_repo = location_name_repo
        ftp_key: str = str(LookupKey.FTP.value)
        sdx_key = str(LookupKey.SDX.value)
        spp_key = str(LookupKey.SPP.value)
        dap_key = str(LookupKey.DAP.value)
        ns5_key = str(LookupKey.NS5.value)
        self._location_keys: dict[str, LocationKey] = {
            ftp_key: {
                "location_type": WINDOWS_SERVER,
                "location_name": self._location_name_repo.get_location_name(LookupKey.FTP)
            },
            sdx_key: {
                "location_type": GCS,
                "location_name": self._location_name_repo.get_location_name(LookupKey.SDX)
            },
            spp_key: {
                "location_type": S3,
                "location_name": self._location_name_repo.get_location_name(LookupKey.SPP)
            },
            dap_key: {
                "location_type": WINDOWS_SERVER,
                "location_name": self._location_name_repo.get_location_name(LookupKey.DAP)
            },
            ns5_key: {
                "location_type": WINDOWS_SERVER,
                "location_name": self._location_name_repo.get_location_name(LookupKey.NS5)
            },
        }

    def get_location_key(self, lookup_key: LookupKey) -> LocationKey:
        return self._location_keys[str(lookup_key.value)]
