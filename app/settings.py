from typing import Annotated

from sdx_base.settings.app import AppSettings, get_settings
from sdx_base.settings.service import SECRET


class Settings(AppSettings):
    data_sensitivity: str
    data_recipient: str
    dap_topic_id: str = "dap-topic"
    dap_public_gpg: Annotated[SECRET, "dap-public-gpg"]
    nifi_location_ftp: Annotated[SECRET, "nifi-location-ftp"]
    nifi_location_spp: Annotated[SECRET, "nifi-location-spp"]
    nifi_location_dap: Annotated[SECRET, "nifi-location-dap"]
    nifi_location_ns5: Annotated[SECRET, "nifi-location-ns5"]
    nifi_location_cdp: Annotated[SECRET, "nifi-location-cdp"]
    nifi_location_ns2: Annotated[SECRET, "nifi-location-ns2"]

    def get_bucket_name(self) -> str:
        return f'{self.project_id}-outputs'


def get_instance() -> Settings:
    return get_settings(Settings)
