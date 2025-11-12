import unittest
from typing import Self

from app.definitions.context import Context, BusinessSurveyContext, AdhocSurveyContext, CommentsFileContext
from app.definitions.context_type import ContextType
from app.definitions.message_schema import Location
from app.definitions.submission_type import SubmissionTypeBase, DECRYPT
from app.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.definitions.survey_type import SurveyType
from app.definitions.zip_details import ZipDetails
from app.services.message_builder import MessageBuilder


class MockSubmissionType(SubmissionTypeBase):
    def get_source(self, filename: str) -> Location:
        return {"location_type": "server1", "location_name": "server1-name", "path": "test-path-1", "filename": filename}

    def get_actions(self) -> list[str]:
        return [DECRYPT]

    def get_outputs(self, filename: str, context: Context) -> list[Location]:
        return [
            {"location_type": "server2", "location_name": "server2-name", "path": "test-path-2", "filename": filename}
        ]


class MockSubmissionTypeMapper(SubmissionTypeMapperBase):
    def get_submission_type(self, survey_type: SurveyType) -> SubmissionTypeBase:
        return MockSubmissionType()


class TestMessageBuilder(unittest.TestCase):
    def setUp(self):
        self.message_builder = MessageBuilder(submission_mapper=MockSubmissionTypeMapper(), data_sensitivity="Low")

    def test_get_source(self: Self):
        filename = "file1"
        source = self.message_builder.get_source(filename, MockSubmissionType())

        expected = {
            "location_type": "server1",
            "location_name": "server1-name",
            "path": "test-path-1",
            "filename": "file1",
        }

        self.assertEqual(expected, source)

    def test_get_target(self: Self):
        filename_list = ["file1", "file2"]
        context: Context = Context(tx_id="123", survey_type=SurveyType.SPP, context_type=ContextType.BUSINESS_SURVEY)
        target_list = self.message_builder.get_targets(filename_list, MockSubmissionType(), context)

        expected = [
            {
                "input": "file1",
                "outputs": [
                    {
                        "location_type": "server2",
                        "location_name": "server2-name",
                        "path": "test-path-2",
                        "filename": "file1",
                    }
                ],
            },
            {
                "input": "file2",
                "outputs": [
                    {
                        "location_type": "server2",
                        "location_name": "server2-name",
                        "path": "test-path-2",
                        "filename": "file2",
                    },
                ],
            },
        ]

        self.assertEqual(expected, target_list)

    def test_get_action(self: Self):
        actions = self.message_builder.get_actions(MockSubmissionType())

        expected = ["decrypt"]
        self.assertEqual(expected, actions)

    def test_get_business_survey_context(self: Self):
        context: BusinessSurveyContext = BusinessSurveyContext(
            tx_id="123",
            survey_type=SurveyType.LEGACY,
            context_type=ContextType.BUSINESS_SURVEY,
            survey_id="666",
            period_id="202101",
            ru_ref="10550",
        )

        actual = self.message_builder.get_context(context)

        expected = {
            "survey_id": "666",
            "period_id": "202101",
            "ru_ref": "10550",
            "context_type": ContextType.BUSINESS_SURVEY,
        }

        self.assertEqual(expected, actual)

    def test_get_comments_context(self: Self):
        context: CommentsFileContext = CommentsFileContext(
            tx_id="123", survey_type=SurveyType.COMMENTS, context_type=ContextType.COMMENTS_FILE, title="Comments.zip"
        )

        actual = self.message_builder.get_context(context)

        expected = {"title": "Comments.zip", "context_type": ContextType.COMMENTS_FILE}

        self.assertEqual(expected, actual)

    def test_get_adhoc_context(self: Self):
        context: AdhocSurveyContext = AdhocSurveyContext(
            tx_id="123",
            survey_type=SurveyType.ADHOC,
            context_type=ContextType.ADHOC_SURVEY,
            survey_id="101",
            title="101 survey response for adhoc survey",
            label="adhoc label",
        )

        actual = self.message_builder.get_context(context)

        expected = {
            "survey_id": "101",
            "title": "101 survey response for adhoc survey",
            "label": "adhoc label",
            "context_type": ContextType.ADHOC_SURVEY,
        }

        self.assertEqual(expected, actual)

    def test_build_message(self: Self):
        input_filename = "input_file"
        filenames = ["file1", "file2"]
        size_bytes = 100
        md5sum = "51252"
        survey_id = "666"
        period_id = "202101"
        ru_ref = "10550"

        context: BusinessSurveyContext = BusinessSurveyContext(
            tx_id="123",
            survey_type=SurveyType.LEGACY,
            context_type=ContextType.BUSINESS_SURVEY,
            survey_id=survey_id,
            period_id=period_id,
            ru_ref=ru_ref,
        )

        zip_details: ZipDetails = {
            "filename": input_filename,
            "size_bytes": size_bytes,
            "md5sum": md5sum,
            "filenames": filenames,
        }

        actual = self.message_builder.build_message(zip_details, context)

        expected = {
            "actions": ["decrypt"],
            "context": {
                "period_id": period_id,
                "ru_ref": ru_ref,
                "survey_id": survey_id,
                "context_type": ContextType.BUSINESS_SURVEY,
            },
            "md5sum": md5sum,
            "schema_version": "2",
            "sensitivity": "Low",
            "sizeBytes": size_bytes,
            "source": {
                "filename": "input_file",
                "location_name": "server1-name",
                "location_type": "server1",
                "path": "test-path-1",
            },
            "targets": [
                {
                    "input": "file1",
                    "outputs": [
                        {
                            "filename": "file1",
                            "location_name": "server2-name",
                            "location_type": "server2",
                            "path": "test-path-2",
                        }
                    ],
                },
                {
                    "input": "file2",
                    "outputs": [
                        {
                            "filename": "file2",
                            "location_name": "server2-name",
                            "location_type": "server2",
                            "path": "test-path-2",
                        }
                    ],
                },
            ],
        }

        self.assertEqual(expected, actual)
