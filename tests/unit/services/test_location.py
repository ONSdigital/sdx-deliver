import unittest
from typing import Final, Self

from app.definitions.location_key import LocationKey, WINDOWS_SERVER, GCS, S3
from app.definitions.lookup_key import LookupKey
from app.services.location import LocationService


NIFI_LOCATION_FTP: Final[str] = "ftp_location_name"
NIFI_LOCATION_SPP: Final[str] = "spp_location_name"
NIFI_LOCATION_DAP: Final[str] = "dap_location_name"
NIFI_LOCATION_NS5: Final[str] = "ns5_location_name"
NIFI_LOCATION_CDP: Final[str] = "cdp_location_name"


class LocationNameSettings:
    project_id = "ons-sdx-sandbox"
    nifi_location_ftp = NIFI_LOCATION_FTP
    nifi_location_spp = NIFI_LOCATION_SPP
    nifi_location_dap = NIFI_LOCATION_DAP
    nifi_location_ns5 = NIFI_LOCATION_NS5
    nifi_location_cdp = NIFI_LOCATION_CDP

    def get_bucket_name(self) -> str:
        return "test-bucket"


class TestLocationService(unittest.TestCase):

    def setUp(self):
        self.location_service = LocationService(LocationNameSettings(), reset=True)

    def test_lookup_ftp(self: Self):
        expected: LocationKey = {
            "location_type": WINDOWS_SERVER,
            "location_name": NIFI_LOCATION_FTP}

        value = self.location_service.get_location_key(LookupKey.FTP)

        self.assertEqual(expected, value)

    def test_lookup_sdx(self: Self):
        expected: LocationKey = {
            "location_type": GCS,
            "location_name": "test-bucket"}

        value = self.location_service.get_location_key(LookupKey.SDX)

        self.assertEqual(expected, value)

    def test_lookup_spp(self: Self):
        expected: LocationKey = {
            "location_type": S3,
            "location_name": NIFI_LOCATION_SPP}

        value = self.location_service.get_location_key(LookupKey.SPP)

        self.assertEqual(expected, value)

    def test_lookup_dap(self: Self):
        expected: LocationKey = {
            "location_type": WINDOWS_SERVER,
            "location_name": NIFI_LOCATION_DAP}

        value = self.location_service.get_location_key(LookupKey.DAP)

        self.assertEqual(expected, value)
