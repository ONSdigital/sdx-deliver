import unittest

from app.v2.definitions.location_key_lookup import LocationKey
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase, LookupKey
from app.v2.location_key_lookup import LocationKeyLookup, WINDOWS_SERVER, GCS, S3


class MockLocationNameRepository(LocationNameRepositoryBase):

    def __init__(self):
        ftp_key = LookupKey.FTP.value
        sdx_key = LookupKey.SDX.value
        spp_key = LookupKey.SPP.value
        dap_key = LookupKey.DAP.value
        ns5_key = LookupKey.NS5.value

        self.locations_mapping = {
            ftp_key: "NIFI_LOCATION_FTP",
            sdx_key: "NIFI_LOCATION_SDX",
            spp_key: "NIFI_LOCATION_SPP",
            dap_key: "NIFI_LOCATION_DAP",
            ns5_key: "NIFI_LOCATION_NS5",
        }

    def get_location_name(self, key: LookupKey) -> str:
        return self.locations_mapping[key.value]

    def load_location_values(self):
        # Not required in mock object
        pass


class TestLocationKeyLookup(unittest.TestCase):

    def test_lookup_ftp(self):
        location_key_lookup = LocationKeyLookup(MockLocationNameRepository())
        expected: LocationKey = {
            "location_type": WINDOWS_SERVER,
            "location_name": "NIFI_LOCATION_FTP"}

        value = location_key_lookup.get_location_key(LookupKey.FTP)

        self.assertEqual(expected, value)

    def test_lookup_sdx(self):
        location_key_lookup = LocationKeyLookup(MockLocationNameRepository())
        expected: LocationKey = {
            "location_type": GCS,
            "location_name": "NIFI_LOCATION_SDX"}

        value = location_key_lookup.get_location_key(LookupKey.SDX)

        self.assertEqual(expected, value)

    def test_lookup_spp(self):
        location_key_lookup = LocationKeyLookup(MockLocationNameRepository())
        expected: LocationKey = {
            "location_type": S3,
            "location_name": "NIFI_LOCATION_SPP"}

        value = location_key_lookup.get_location_key(LookupKey.SPP)

        self.assertEqual(expected, value)

    def test_lookup_dap(self):
        location_key_lookup = LocationKeyLookup(MockLocationNameRepository())
        expected: LocationKey = {
            "location_type": WINDOWS_SERVER,
            "location_name": "NIFI_LOCATION_DAP"}

        value = location_key_lookup.get_location_key(LookupKey.DAP)

        self.assertEqual(expected, value)
