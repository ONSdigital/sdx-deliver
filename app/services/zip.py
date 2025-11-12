import zipfile

import io

from app.definitions.zip import ZipBase


class ZipService(ZipBase):
    def unzip(self, data_bytes: bytes) -> list[str]:
        # Create a BytesIO object from the bytes
        zip_file = io.BytesIO(data_bytes)

        # Open the zip file
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            # List the filenames of the zip file
            return zip_ref.namelist()
