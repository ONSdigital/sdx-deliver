from typing import TypedDict


class Location(TypedDict):
    location_type: str
    location_name: str


class Actions: list[str]


class File(TypedDict):
    location: str
    path: str


class SubmissionType(TypedDict):
    actions: list[str]
    source: File
    outputs: list[dict[str, File]]


class ConfigSchema(TypedDict):
    locations: dict[str, Location]
    submission_type: dict[str, SubmissionType]