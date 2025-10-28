from enum import StrEnum


class SurveyType(StrEnum):
    DAP = "dap"
    LEGACY = "legacy"
    SPP = "spp"
    ENVIRONMENTAL = "environmental"
    MATERIALS = "materials"
    FEEDBACK = "feedback"
    SEFT = "seft"
    ADHOC = "adhoc"
    COMMENTS = "comments"
    DEXTA = "dexta"
