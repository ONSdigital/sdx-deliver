from app import sdx_app, CONFIG
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase, LookupKey

NIFI_LOCATION_FTP = "nifi-location-ftp"
NIFI_LOCATION_SPP = "nifi-location-spp"
NIFI_LOCATION_DAP = "nifi-location-dap"


class LocationNameRepo(LocationNameRepositoryBase):

    def __init__(self):
        self.locations_mapping = None

    def get_location_name(self, key: LookupKey) -> str:
        return self.locations_mapping[key.value]

    def load_location_values(self):
        if self.locations_mapping is None:
            ftp_key = LookupKey.FTP.value
            sdx_key = LookupKey.SDX.value
            spp_key = LookupKey.SPP.value
            dap_key = LookupKey.DAP.value

            self.locations_mapping = {
                ftp_key: sdx_app.secrets_get(NIFI_LOCATION_FTP)[0],
                sdx_key: CONFIG.BUCKET_NAME,
                spp_key: sdx_app.secrets_get(NIFI_LOCATION_SPP)[0],
                dap_key: sdx_app.secrets_get(NIFI_LOCATION_DAP)[0]
            }
