from typing import Annotated

from sdx_base.settings.app import AppSettings, get_settings
from sdx_base.settings.service import SECRET

from app.definitions.lookup_key import LookupKey


class Settings(AppSettings):
    data_sensitivity: str
    data_recipient: str
    bucket_name: str
    dap_topic_id: str = "dap-topic"
    dap_public_gpg: Annotated[SECRET, "dap-public-gpg"]
    nifi_location_ftp: Annotated[SECRET, "nifi-location-ftp"]
    nifi_location_spp: Annotated[SECRET, "nifi-location-spp"]
    nifi_location_dap: Annotated[SECRET, "nifi-location-dap"]
    nifi_location_ns5: Annotated[SECRET, "nifi-location-ns5"]

    def get_gpg_key(self) -> str:
        return self.dap_public_gpg

    def get_data_recipient(self) -> str:
        return self.data_recipient

    def get_bucket_name(self) -> str:
        return f'{self.project_id}-outputs'

    def get_location_name(self, key: LookupKey) -> str:
        if key == LookupKey.FTP:
            return self.nifi_location_ftp
        elif key == LookupKey.SPP:
            return self.nifi_location_spp
        elif key == LookupKey.DAP:
            return self.nifi_location_dap
        elif key == LookupKey.NS5:
            return self.nifi_location_ns5
        else:
            # return sdx location
            return self.get_bucket_name()


def get_instance() -> Settings:
    return get_settings(Settings)