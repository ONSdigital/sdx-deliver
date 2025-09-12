from typing import TypedDict

from app.definitions.context_type import ContextType
from app.definitions.survey_type import SurveyType


class Context(TypedDict):
    tx_id: str
    survey_type: SurveyType
    context_type: ContextType


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
