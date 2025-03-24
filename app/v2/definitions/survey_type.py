from enum import StrEnum


class SurveyType(StrEnum):
    DAP = "dap"
    LEGACY = "legacy"
    SPP = "spp"
    NS5 = "ns5"
    FEEDBACK = "feedback"
    SEFT = "seft"
    ADHOC = "adhoc"
    COMMENTS = "comments"
