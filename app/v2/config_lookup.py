from typing import Final

from app.v2.definitions.config_schema import ConfigSchema, File, LocationKey
from app.v2.definitions.location_key_lookup import LocationKeyLookupBase
from app.v2.definitions.location_name_repository import LookupKey
from app.v2.definitions.message_schema import Location

LOCATION_TYPE: Final[str] = "location_type"
LOCATION_NAME: Final[str] = "location_name"
LOCATIONS: Final[str] = "locations"
SUBMISSION_TYPES: Final[str] = "submission_types"


class ConfigLookup:

    def __init__(self, config_schema: ConfigSchema, location_key_lookup: LocationKeyLookupBase):
        self._config_schema = config_schema
        self._location_key_lookup = location_key_lookup

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

    def _get_location_details(self, file: File) -> LocationKey:
        lookup_key: LookupKey = file["location"]
        return self._location_key_lookup.get_location_key(lookup_key)
    