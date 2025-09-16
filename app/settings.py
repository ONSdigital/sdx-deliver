from typing import Annotated

from sdx_base.settings.app import AppSettings, get_settings
from sdx_base.settings.service import SECRET


class Settings(AppSettings):
    data_sensitivity: str
    data_recipient: str
    bucket_name: str
    dap_topic_id: str = "dap-topic"
    dap_public_gpg: Annotated[SECRET, "dap-public-gpg"]
    encryption_key_set: bool = False

    def get_bucket_name(self) -> str:
        return f'{self.project_id}-outputs'


def settings() -> Settings:
    return get_settings(Settings)