from typing import Final

from app.v2.definitions.location_name_repository import LocationNameRepositoryBase, LookupKey


SDX_LOCATION_NAME: Final[str] = "sdx_location_name"
FTP_LOCATION_NAME: Final[str] = "ftp_location_name"
SPP_LOCATION_NAME: Final[str] = "spp_location_name"
DAP_LOCATION_NAME: Final[str] = "dap_location_name"
NS5_LOCATION_NAME: Final[str] = "ns5_location_name"


class MockLocationNameMapper(LocationNameRepositoryBase):
    def __init__(self):
        self.locations_mapping = None

    def get_location_name(self, key: LookupKey) -> str:
        return self.locations_mapping[key.value]

    def load_location_values(self):
        ftp_key = LookupKey.FTP.value
        sdx_key = LookupKey.SDX.value
        spp_key = LookupKey.SPP.value
        dap_key = LookupKey.DAP.value
        ns5_key = LookupKey.NS5.value
        self.locations_mapping = {
            ftp_key: FTP_LOCATION_NAME,
            sdx_key: SDX_LOCATION_NAME,
            spp_key: SPP_LOCATION_NAME,
            dap_key: DAP_LOCATION_NAME,
            ns5_key: NS5_LOCATION_NAME,
        }


class FileHolder:

    def __init__(self, file_bytes: bytes):
        self._file_bytes = file_bytes

    def read(self) -> bytes:
        return self._file_bytes
