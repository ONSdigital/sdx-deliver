from enum import StrEnum


class SurveyType(StrEnum):
    EQV1JSON = "eqv1json"
    LEGACY = "legacy"
    SPPJSON_IMG_RCPT = "sppjson_img_rcpt"
    EQV1JSON_IMG_RCPT = "eqv1json_img_rcpt"
    EQV2JSON_IMG_RCPT = "eqv2json_img_rcpt"
    FEEDBACK = "feedback"
    SEFT = "seft"
    SEFT_RCPT = "seft_rcpt"
    EQV2JSON = "eqv2json"
    COMMENTS = "comments"
    PCK_IMG_RCPT = "pck_img_rcpt"
