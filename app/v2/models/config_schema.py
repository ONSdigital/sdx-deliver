from typing import TypedDict


class LocationDetails(TypedDict):
    location_type: str
    location_name: str


class File(TypedDict):
    location: str
    path: str


class SubmissionType(TypedDict):
    actions: list[str]
    source: File
    outputs: dict[str, list[File]]


class ConfigSchema(TypedDict):
    locations: dict[str, LocationDetails]
    submission_types: dict[str, SubmissionType]
