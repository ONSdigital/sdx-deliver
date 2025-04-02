from typing import TypedDict, NotRequired


class FilesSchema(TypedDict):
    name: str
    sizeBytes: int
    md5sum: str


class MessageSchema(TypedDict):
    version: str
    files: list[FilesSchema]
    sensitivity: str
    sourceName: str
    manifestCreated: str
    description: str
    dataset: str
    schemaversion: str
    iterationL1: NotRequired[str]
    iterationL2: NotRequired[str]
