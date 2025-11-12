from typing import Protocol, Final

from sdx_base.settings.service import SECRET
from sdx_base.utilities.singleton import AbstractSingleton

from app.definitions.location import LocationBase
from app.definitions.location_key import WINDOWS_SERVER, GCS, S3, LocationKey, CDP
from app.definitions.lookup_key import LookupKey


PROD_PROJECT: Final[str] = "ons-sdx-prod"


class LocationNameSettings(Protocol):
    project_id: str
    nifi_location_ftp: SECRET
    nifi_location_spp: SECRET
    nifi_location_dap: SECRET
    nifi_location_ns5: SECRET
    nifi_location_cdp: SECRET
    nifi_location_ns2: SECRET

    def get_bucket_name(self) -> str: ...


class LocationService(LocationBase, metaclass=AbstractSingleton):
    def __init__(self, location_name_settings: LocationNameSettings):
        self._settings = location_name_settings
        ftp_key: str = str(LookupKey.FTP.value)
        sdx_key: str = str(LookupKey.SDX.value)
        spp_key: str = str(LookupKey.SPP.value)
        dap_key: str = str(LookupKey.DAP.value)
        ns5_key: str = str(LookupKey.NS5.value)
        cdp_key: str = str(LookupKey.CDP.value)
        ns2_key: str = str(LookupKey.NS2.value)
        self._location_keys: dict[str, LocationKey] = {
            ftp_key: {"location_type": WINDOWS_SERVER, "location_name": self._get_location_name(LookupKey.FTP)},
            sdx_key: {"location_type": GCS, "location_name": self._get_location_name(LookupKey.SDX)},
            spp_key: {"location_type": S3, "location_name": self._get_location_name(LookupKey.SPP)},
            dap_key: {"location_type": WINDOWS_SERVER, "location_name": self._get_location_name(LookupKey.DAP)},
            ns5_key: {"location_type": WINDOWS_SERVER, "location_name": self._get_location_name(LookupKey.NS5)},
            ns2_key: {"location_type": WINDOWS_SERVER, "location_name": self._get_location_name(LookupKey.NS2)},
            cdp_key: {"location_type": CDP, "location_name": self._get_location_name(LookupKey.CDP)},
        }

    def _get_location_name(self, key: LookupKey) -> str:
        if key == LookupKey.FTP:
            return self._settings.nifi_location_ftp
        elif key == LookupKey.SPP:
            return self._settings.nifi_location_spp
        elif key == LookupKey.DAP:
            return self._settings.nifi_location_dap
        elif key == LookupKey.NS5:
            return self._settings.nifi_location_ns5
        elif key == LookupKey.NS2:
            return self._settings.nifi_location_ns2
        elif key == LookupKey.CDP:
            return self._settings.nifi_location_cdp
        else:
            # return sdx location
            return self._settings.get_bucket_name()

    def is_prod_env(self) -> bool:
        return self._settings.project_id == PROD_PROJECT

    def get_location_key(self, lookup_key: LookupKey) -> LocationKey:
        return self._location_keys[str(lookup_key.value)]
