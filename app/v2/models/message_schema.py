from typing import TypedDict
from enum import Enum


class Location(TypedDict):
    location_type: str
    location_name: str
    path: str
    filename: str


class Target(TypedDict):
    input: str
    outputs: list[Location]


class Context(TypedDict):
    context_type: str


class SchemaDataV2(TypedDict):
    schema_version: str
    sensitivity: str
    sizeBytes: int
    md5sum: str
    context: Context
    source: Location
    actions: list[str]
    targets: list[Target]


class Filetype(Enum):
    image = "image"
    index = "index"
    receipt = "receipt"
    pck = "pck"
