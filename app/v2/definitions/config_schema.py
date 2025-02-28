from typing import TypedDict

from app.v2.definitions.location_name_repository import LookupKey


class File(TypedDict):
    location: LookupKey
    path: str
