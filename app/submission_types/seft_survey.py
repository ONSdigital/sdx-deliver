from typing import Final, override, cast, Protocol

from app.definitions.config_schema import File
from app.definitions.context import BusinessSurveyContext, Context
from app.definitions.submission_type import DECRYPT
from app.services.output_mapper.output_mapper_configs import SEFTOutputConfigPreProd
from app.submission_types.bases.submission_type import SubmissionType, LocationHelper

_XLSX: Final[str] = "xlsx"


class SeftSubmissionType(SubmissionType):
    def __init__(self, location_helper: LocationHelper, output_mapper: SEFTOutputConfigPreProd) -> None:
        super().__init__(location_helper)
        self._output_mapper = output_mapper

    @override
    def get_source_path(self) -> str:
        return "seft"

    @override
    def get_actions(self) -> list[str]:
        return [DECRYPT]

    @override
    def create_file_config(self, context: Context) -> dict[str, list[File]]:
        business_context: BusinessSurveyContext = cast(BusinessSurveyContext, context)
        return self.get_file_config(business_context)

    def get_file_config(self, context: BusinessSurveyContext) -> dict[str, list[File]]:
        return {
            _XLSX: [self._output_mapper.map_output(context, self._is_prod_env())]
        }

    @override
    def get_mapping(self, filename: str) -> str:
        return _XLSX

    @override
    def get_output_filename(self, filename: str, _context: Context) -> str:
        # remove the .gpg extension
        return filename[:-4]
