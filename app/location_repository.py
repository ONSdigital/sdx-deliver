from models import Location, Filetype


class LocationRepository:
    def __init__(self, path_mapping: dict[Filetype, str] ):
        self._path_mapping = path_mapping


    def get_ftp_server(self, file_type: Filetype, filename: str) -> Location:
        return Location(
            location_type="windows_server",
            location_name="NP123456",
            path=self._path_mapping[file_type],
            filename=filename
        )
    

    def get_spp_landing_zone(self, survey_id: str, filename: str) -> Location:
        return Location(
            location_type="s3",
            location_name="spp-bucket-name",
            path=f"sdc-response/{survey_id}",
            filename=filename
        )
        pass


    def get_dap(self) -> Location:
        pass
