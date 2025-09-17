from typing import TypedDict

from app.definitions.lookup_key import LookupKey


class File(TypedDict):
    location: LookupKey
    path: str
