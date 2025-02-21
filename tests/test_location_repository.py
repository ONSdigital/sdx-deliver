import unittest

from app.v2.models.message_schema import Location, Filetype
from app.location_repository import LocationRepository


class TestLocationRepository(unittest.TestCase):
    def setUp(self):
        self.location_repository = LocationRepository(path_mapping={
            "image": "SDX_PREPROD/EDC_QImages/Images",
            "index": "SDX_PREPROD/EDC_QImages/Index",
            "receipt": "SDX_PREPROD/EDC_QReceipts",
            "pck": "SDX_PREPROD/EDC_QData"
        })

    def test_get_ftp_server(self):
        pass

    def test_get_spp_landing_zone(self):
        survey_id = "009"
        filename = "009_7f64de4907da4065.json"

        location: Location = self.location_repository.get_spp_landing_zone(survey_id=survey_id, filename=filename)
        self.assertEqual(location, {
            "location_type": "s3",
            "location_name": "spp-bucket-name",
            "path": "sdc-response/009",
            "filename": "009_7f64de4907da4065.json"
          }
        )

    def test_get_dap(self):
        pass

    def test_get_image_location(self):

        location: Location = self.location_repository.get_ftp_server(file_type=Filetype.image, filename="S_7f64de4907da4065.jpg")
        self.assertEqual(location, {
            "location_type": "windows_server",
            "location_name": "NP123456",
            "path": "SDX_PREPROD/EDC_QImages/Images",
            "filename": "S_7f64de4907da4065.jpg"
          }
        )

    def test_get_index_location(self):

        location: Location = self.location_repository.get_ftp_server(file_type=Filetype.index, filename="EDC_202_7f64de4907da4065.csv")
        self.assertEqual(location, {
            "location_type": "windows_server",
            "location_name": "NP123456",
            "path": "SDX_PREPROD/EDC_QImages/Index",
            "filename": "EDC_202_7f64de4907da4065.csv"
          }
        )

    def test_get_receipt_location(self):

        location: Location = self.location_repository.get_ftp_server(file_type=Filetype.receipt, filename="REC0202_7f64de4907da4065.dat")
        self.assertEqual(location, {
            "location_type": "windows_server",
            "location_name": "NP123456",
            "path": "SDX_PREPROD/EDC_QReceipts",
            "filename": "REC0202_7f64de4907da4065.dat"
          }
        )

    def test_get_pck_location(self):

        location: Location = self.location_repository.get_ftp_server(file_type=Filetype.pck, filename="202_7f64de4907da4065")
        self.assertEqual(location, {
            "location_type": "windows_server",
            "location_name": "NP123456",
            "path": "SDX_PREPROD/EDC_QData",
            "filename": "202_7f64de4907da4065"
          }
        )
