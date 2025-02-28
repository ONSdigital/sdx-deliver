from typing import TypedDict


class Location(TypedDict):
    location_type: str
    location_name: str
    path: str
    filename: str


class Target(TypedDict):
    input: str
    outputs: list[Location]


class SchemaDataV2(TypedDict):
    schema_version: str
    sensitivity: str
    sizeBytes: int
    md5sum: str
    context: dict[str, str]
    source: Location
    actions: list[str]
    targets: list[Target]
