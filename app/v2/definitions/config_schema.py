from typing import TypedDict

from app.v2.definitions.location_name_repository import LookupKey


class LocationKey(TypedDict):
    location_type: str
    location_name: str


class File(TypedDict):
    location: LookupKey
    path: str


class SubmissionType(TypedDict):
    actions: list[str]
    source: File
    outputs: dict[str, list[File]]


class ConfigSchema(TypedDict):
    submission_types: dict[str, SubmissionType]
