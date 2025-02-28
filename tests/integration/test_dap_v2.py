import json
import unittest
from typing import Final
from unittest.mock import patch, Mock

from sdx_gcp import Request

from app import deliver
from app.routes import FILE_NAME, VERSION, V2, SUBMISSION_FILE, MESSAGE_SCHEMA, deliver_dap
from app.v2.definitions.location_name_repository import LocationNameRepositoryBase, LookupKey
from app.v2.definitions.message_schema import SchemaDataV2

SDX_LOCATION_NAME: Final[str] = "sdx_location_name"
FTP_LOCATION_NAME: Final[str] = "ftp_location_name"
SPP_LOCATION_NAME: Final[str] = "spp_location_name"
DAP_LOCATION_NAME: Final[str] = "dap_location_name"


class MockLocationNameMapper(LocationNameRepositoryBase):
    def __init__(self):
        self.locations_mapping = None

    def get_location_name(self, key: LookupKey) -> str:
        return self.locations_mapping[key.value]

    def load_location_values(self):
        ftp_key = LookupKey.FTP.value
        sdx_key = LookupKey.SDX.value
        spp_key = LookupKey.SPP.value
        dap_key = LookupKey.DAP.value
        self.locations_mapping = {
            ftp_key: FTP_LOCATION_NAME,
            sdx_key: SDX_LOCATION_NAME,
            spp_key: SPP_LOCATION_NAME,
            dap_key: DAP_LOCATION_NAME
        }


class FileHolder:

    def __init__(self, file_bytes: bytes):
        self._file_bytes = file_bytes

    def read(self) -> bytes:
        return self._file_bytes


class TestDapV2(unittest.TestCase):

    @patch('app.deliver.write_to_bucket')
    @patch('app.deliver.publish_v2_schema')
    @patch('app.deliver.encrypt_output')
    @patch('app.routes.Flask.jsonify')
    def test_dap(self,
                 mock_jsonify: Mock,
                 mock_encrypt: Mock,
                 mock_publish_v2_schema: Mock,
                 mock_write_to_bucket: Mock):
        deliver.location_name_repo = MockLocationNameMapper()
        mock_encrypt.return_value = "My encrypted output"
        mock_write_to_bucket.return_value = "My fake bucket path"
        mock_jsonify.return_value = {"success": True}

        tx_id = "016931f2-6230-4ca3-b84e-136e02e3f92b"
        input_filename = "016931f2-6230-4ca3-b84e-136e02e3f92b.json"
        output_filename = input_filename
        survey_id = "009"
        period_id = "202505"
        ruref = "49900000001A"

        submission_file = {
            "tx_id": tx_id,
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "v2",
            "data_version": "0.0.3",
            "origin": "uk.gov.ons.edc.eq",
            "flushed": False,
            "submitted_at": "2016-05-21T16:37:56.551086",
            "launch_language_code": "en",
            "submission_language_code": "en",
            "collection_exercise_sid": "9ced8dc9-f2f3-49f3-95af-2f3ca0b74ee3",
            "schema_name": "mbs_0001",
            "started_at": "2016-05-21T16:33:30.665144",
            "case_id": "a386b2de-a615-42c8-a0f4-e274f9eb28ee",
            "region_code": "GB-ENG",
            "channel": "RAS",
            "survey_metadata": {
                "survey_id": survey_id,
                "case_ref": "1000000000000001",
                "case_type": "B",
                "display_address": "ONS, Government Buildings, Cardiff Rd",
                "employment_date": "2021-03-01",
                "form_type": "0253",
                "period_id": period_id,
                "period_str": "January 2021",
                "ref_p_end_date": "2021-06-01",
                "ref_p_start_date": "2021-01-01",
                "ru_name": "ACME T&T Limited",
                "ru_ref": ruref,
                "trad_as": "ACME LTD.",
                "user_id": "64389274239"
            },
            "data": {
                "answers": [
                    {
                        "answer_id": "first-name",
                        "value": "John",
                        "list_item_id": "zGBdpb"
                    },
                    {
                        "answer_id": "last-name",
                        "value": "Doe",
                        "list_item_id": "zGBdpb"
                    },
                    {
                        "answer_id": "first-name",
                        "value": "Marie",
                        "list_item_id": "cWGwcF"
                    },
                    {
                        "answer_id": "last-name",
                        "value": "Doe",
                        "list_item_id": "cWGwcF"
                    },
                    {
                        "answer_id": "anyone-else",
                        "value": "No"
                    },
                    {
                        "answer_id": "number-of-bedrooms-answer",
                        "value": 4
                    },
                    {
                        "answer_id": "date-of-birth-answer",
                        "value": "1990-01-01",
                        "list_item_id": "EINoLs"
                    },
                    {
                        "answer_id": "internet-answer",
                        "value": [
                            "Broadband or WiFi",
                            "A mobile phone network such as 3G, 4G or 5G",
                            "Public WiFi hotspot"
                        ]
                    },
                    {
                        "answer_id": "business-type-answer",
                        "value": "Enter Business type here!",
                        "list_item_id": "EINoLs"
                    },
                    {
                        "answer_id": "relationship-answer",
                        "value": [
                            {
                                "list_item_id": "zGBdpb",
                                "to_list_item_id": "cWGwcF",
                                "relationship": "Husband or Wife"
                            },
                            {
                                "list_item_id": "nEMpwe",
                                "to_list_item_id": "adNCSi",
                                "relationship": "Son or daughter"
                            },
                            {
                                "list_item_id": "ukGiCK",
                                "to_list_item_id": "adNCSi",
                                "relationship": "Mother or father"
                            }
                        ]
                    },
                    {
                        "answer_id": "other-address-uk-answer",
                        "value": {
                            "line1": "Address Line 1",
                            "town": "Town",
                            "postcode": "NP10 8XG",
                            "uprn": "12345678912"
                        },
                        "list_item_id": "cWGwcF"
                    },
                    {
                        "answer_id": "checkbox-answer",
                        "value": ["Checkbox 1", "Checkbox 2"]
                    },
                    {
                        "answer_id": "duration-answer",
                        "value": {
                            "years": 1,
                            "months": 2
                        }
                    }
                ],
                "lists": [
                    {
                        "items": ["zGBdpb", "cWGwcF"],
                        "name": "people"
                    }
                ]
            }
        }

        # Create the fake Request object

        files_dict = {
            SUBMISSION_FILE: FileHolder(json.dumps(submission_file).encode("utf-8")),
        }

        data = {
            FILE_NAME: input_filename,
            "tx_id": tx_id,
            VERSION: V2,
            MESSAGE_SCHEMA: V2
        }

        class MockRequest(Request):
            files = files_dict
            args = data

        # Call the endpoint
        response = deliver_dap(MockRequest(data), tx_id)
        self.assertTrue(response["success"])

        expected_v2_message: SchemaDataV2 = {
            "schema_version": "2",
            "sensitivity": "High",
            "sizeBytes": 19,
            "md5sum": "3190f8a68aad6a9e33a624c318516ebb",
            "context": {
                "survey_id": survey_id,
                "period_id": period_id,
                "ru_ref": ruref
            },
            "source": {
                "location_type": "gcs",
                "location_name": SDX_LOCATION_NAME,
                "path": "dap",
                "filename": input_filename
            },
            "actions": ["decrypt"],
            "targets": [
                {
                    "input": input_filename,
                    "outputs": [
                        {
                            "location_type": "cdp",
                            "location_name": DAP_LOCATION_NAME,
                            "path": f"landing_zone/sdx_preprod/{survey_id}",
                            "filename": output_filename
                        }
                    ]
                }
            ]
        }

        mock_publish_v2_schema.assert_called_with(expected_v2_message, tx_id)
