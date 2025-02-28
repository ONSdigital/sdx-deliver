from app.v2.definitions.config_schema import LocationKey
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase, LookupKey
from app.v2.message_config import WINDOWS_SERVER, GCS, S3, CDP


class LocationKeyLookup(LocationKeyLookupBase):

    def __init__(self, location_name_repo: LocationNameRepositoryBase):
        self._location_name_repo = location_name_repo
        ftp_key = LookupKey.FTP.value
        sdx_key = LookupKey.SDX.value
        spp_key = LookupKey.SPP.value
        dap_key = LookupKey.DAP.value
        self._location_keys = {
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
                "location_type": CDP,
                "location_name": self._location_name_repo.get_location_name(LookupKey.DAP)
            }
        }

    def get_location_key(self, lookup_key: LookupKey) -> LocationKey:
        return self._location_keys[lookup_key.value]
