from typing import cast

from app.definitions.context import Context, CommentsFileContext, AdhocSurveyContext, BusinessSurveyContext
from app.definitions.context_type import ContextType
from app.definitions.message_builder import MessageBuilderBase
from app.definitions.message_schema import MessageSchemaV2, Location, Target
from app.definitions.submission_type import SubmissionTypeBase
from app.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.definitions.zip_details import ZipDetails


class MessageBuilder(MessageBuilderBase):

    def __init__(self, submission_mapper: SubmissionTypeMapperBase, data_sensitivity: str):
        self._submission_mapper = submission_mapper
        self._data_sensitivity = data_sensitivity

    def build_message(self, zip_details: ZipDetails, context: Context) -> MessageSchemaV2:
        submission_type: SubmissionTypeBase = self._submission_mapper.get_submission_type(context.survey_type)
        message: MessageSchemaV2 = {
            "schema_version": "2",
            "sensitivity": self._data_sensitivity,
            "sizeBytes": zip_details["size_bytes"],
            "md5sum": zip_details["md5sum"],
            "context": self.get_context(context),
            "source": self.get_source(zip_details["filename"], submission_type),
            "actions": self.get_actions(submission_type),
            "targets": self.get_targets(zip_details["filenames"], submission_type, context)
        }
        return message

    def get_source(self, filename: str, submission_type: SubmissionTypeBase) -> Location:
        location = submission_type.get_source(filename)
        return location

    def get_targets(self, filenames: list[str], submission_type: SubmissionTypeBase, context: Context) -> list[Target]:
        target_list: list[Target] = []
        for filename in filenames:
            outputs: list[Location] = submission_type.get_outputs(filename, context)
            target_list.append({"input": filename, "outputs": outputs})

        return target_list

    def get_actions(self, submission_type: SubmissionTypeBase) -> list[str]:
        return submission_type.get_actions()

    def get_context(self, context: Context) -> dict[str, str]:
        if context.context_type == ContextType.COMMENTS_FILE:
            comments_context: CommentsFileContext = cast(CommentsFileContext, context)
            return {
                "title": "Comments.zip",
                "context_type": comments_context.context_type
            }

        elif context.context_type == ContextType.ADHOC_SURVEY:
            adhoc_context: AdhocSurveyContext = cast(AdhocSurveyContext, context)
            return {
                "survey_id": adhoc_context.survey_id,
                "title": adhoc_context.title,
                "label": adhoc_context.label,
                "context_type": adhoc_context.context_type
            }

        else:
            business_context: BusinessSurveyContext = cast(BusinessSurveyContext, context)
            return {
                "survey_id": business_context.survey_id,
                "period_id": business_context.period_id,
                "ru_ref": business_context.ru_ref,
                "context_type": business_context.context_type
            }
