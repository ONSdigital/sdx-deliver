from typing import TypedDict


class ZipDetails(TypedDict):
    filename: str
    size_bytes: int
    md5sum: str
    filenames: list[str]
