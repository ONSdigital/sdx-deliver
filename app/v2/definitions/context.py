from typing import TypedDict

from app.v2.definitions.survey_type import SurveyType


class Context(TypedDict):
    tx_id: str
    survey_type: SurveyType


class BusinessSurveyContext(Context):
    survey_id: str
    period_id: str
    ru_ref: str


class AdhocSurveyContext(Context):
    survey_id: str
    title: str
    label: str


class CommentsFileContext(Context):
    title: str
