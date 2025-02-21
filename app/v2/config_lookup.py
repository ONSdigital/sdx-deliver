from typing import Final

from app.v2.models.config_schema import ConfigSchema, File, LocationDetails
from app.v2.models.message_schema import Location


LOCATION_TYPE: Final[str] = "location_type"
LOCATION_NAME: Final[str] = "location_name"
LOCATIONS: Final[str] = "locations"
SUBMISSION_TYPES: Final[str] = "submission_types"


class ConfigLookup:

    def __init__(self, config_schema: ConfigSchema):
        self._config_schema = config_schema

    def get_source(self, submission_type: str, filename: str) -> Location:
        source = self._config_schema[SUBMISSION_TYPES][submission_type]["source"]
        loc_details = self._get_location_details(source)

        return {
            "location_type": loc_details[LOCATION_TYPE],
            "location_name": loc_details[LOCATION_NAME],
            "path": source["path"],
            "filename": filename
        }

    def get_actions(self, submission_type: str) -> list[str]:
        return self._config_schema[SUBMISSION_TYPES][submission_type]["actions"]

    def get_outputs(self, submission_type: str, output_type: str, filename: str) -> list[Location]:
        outputs = self._config_schema[SUBMISSION_TYPES][submission_type]["outputs"]
        outputs_list = outputs[output_type]
        results: list[Location] = []

        for output in outputs_list:
            loc_details = self._get_location_details(output)

            results.append({
                "location_type": loc_details[LOCATION_TYPE],
                "location_name": loc_details[LOCATION_NAME],
                "path": output["path"],
                "filename": filename
            })

        return results

    def _get_location_details(self, file: File) -> LocationDetails:
        location = file["location"]
        return self._config_schema[LOCATIONS][location]
    