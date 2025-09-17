from typing import Protocol

from app.definitions.location_key import WINDOWS_SERVER, GCS, S3, LocationKey
from app.definitions.lookup_key import LookupKey


class LocationNameFinder(Protocol):
    def get_location_name(self, key: LookupKey) -> str: ...


class LocationKeyLookup:

    def __init__(self, location_name_finder: LocationNameFinder):
        self._location_name_repo = location_name_finder
        ftp_key: str = str(LookupKey.FTP.value)
        sdx_key: str = str(LookupKey.SDX.value)
        spp_key: str = str(LookupKey.SPP.value)
        dap_key: str = str(LookupKey.DAP.value)
        ns5_key: str = str(LookupKey.NS5.value)
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
