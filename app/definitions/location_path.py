from typing import TypedDict

from app.definitions.lookup_key import LookupKey


class LocationPath(TypedDict):
    location: LookupKey
    path: str
