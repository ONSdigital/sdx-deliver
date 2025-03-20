from typing import TypedDict

from app import CONFIG
from app.meta_wrapper import MetaWrapper, MetaWrapperAdhoc
from app.output_type import OutputType
from app.routes_v2 import BusinessSurveyContext
from app.v2.definitions.message_schema import MessageSchemaV2, Target, Location
from app.v2.definitions.submission_type import SubmissionTypeBase
from app.v2.definitions.submission_type_mapper import SubmissionTypeMapperBase


class ZipDetails(TypedDict):
    size_bytes: int
    md5sum: str


class MessageBuilder:

    def __init__(self, submission_mapper: SubmissionTypeMapperBase):
        self._submission_mapper = submission_mapper

    def build_message(self, filenames: list[str], zip_details: ZipDetails, context: BusinessSurveyContext) -> MessageSchemaV2:
        submission_type: SubmissionTypeBase = self._submission_mapper.get_submission_type(meta_data.output_type)
        message: MessageSchemaV2 = {
            "schema_version": "2",
            "sensitivity": CONFIG.DATA_SENSITIVITY,
            "sizeBytes": meta_data.sizeBytes,
            "md5sum": meta_data.md5sum,
            "context": self.get_context(meta_data),
            "source": self.get_source(meta_data.output_filename, submission_type),
            "actions": self.get_actions(submission_type),
            "targets": self.get_targets(filenames, submission_type, meta_data)
        }
        return message

    def get_source(self, filename: str, submission_type: SubmissionTypeBase) -> Location:
        location = submission_type.get_source(filename)
        return location

    def get_targets(self, filenames: list[str], submission_type: SubmissionTypeBase, meta_data: MetaWrapper) -> list[Target]:
        target_list: list[Target] = []
        for filename in filenames:
            outputs: list[Location] = submission_type.get_outputs(filename, meta_data)
            target_list.append({"input": filename, "outputs": outputs})

        return target_list

    def get_actions(self, submission_type: SubmissionTypeBase) -> list[str]:
        return submission_type.get_actions()
    
    def get_context(self, meta_data: MetaWrapper) -> dict[str, str]:
        if meta_data.output_type == OutputType.COMMENTS:
            return {
                "title": "Comments.zip"
            }
        
        if isinstance(meta_data, MetaWrapperAdhoc):
            return {
                "survey_id": meta_data.survey_id,
                "title": meta_data.get_description()
            }

        return {
            "survey_id": meta_data.survey_id,
            "period_id": meta_data.period,
            "ru_ref": meta_data.ru_ref,
        }
