from enum import StrEnum


class SurveyType(StrEnum):
    DAP = "dap"
    LEGACY = "legacy"
    SPP = "spp"
    ENVIRONMENTAL = "environmental"
    MATERIALS = "materials"
    FEEDBACK = "feedback"
    SEFT = "seft"
    SEFT_RECEIPT = "seft_receipt"
    ADHOC = "adhoc"
    COMMENTS = "comments"
    DEXTA = "dexta"
