from datetime import datetime

from sdx_gcp.errors import DataError

from app.output_type import OutputType


locations = {
    "DAP": "dap",
    "FTP": "ftp",
    "HYBRID": "hybrid"
}


def _get_field(survey_dict: dict, *field_names: str) -> str:
    current = survey_dict
    for key in field_names:
        current = current.get(key)
        if not current:
            raise DataError(f'Missing field {key} from response!')
    return current


class MetaWrapper:

    """
    This class provides a common interface to the metadata associated with different types of survey submissions
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.tx_id = None
        self.survey_id = None
        self.period = None
        self.ru_ref = None
        self.md5sum = None
        self.sizeBytes = 0
        self.output_type = None

    def _from_survey(self, survey_dict: dict):
        self.tx_id = _get_field(survey_dict, 'tx_id')
        self.survey_id = _get_field(survey_dict, 'survey_id')
        self.period = _get_field(survey_dict, 'collection', 'period')
        self.ru_ref = _get_field(survey_dict, 'metadata', 'ru_ref')

    def set_legacy(self, survey_dict: dict):
        self.filename = f'{self.filename}:{locations["FTP"]}'
        self.output_type = OutputType.LEGACY
        self._from_survey(survey_dict)

    def set_hybrid(self, survey_dict: dict):
        self.filename = f'{self.filename}:{locations["HYBRID"]}'
        self.output_type = OutputType.HYBRID
        self._from_survey(survey_dict)

    def set_dap(self, survey_dict: dict):
        self.filename = f'{self.filename}.json:{locations["DAP"]}'
        self.output_type = OutputType.DAP
        self._from_survey(survey_dict)

    def set_feedback(self, survey_dict: dict):
        postfix = datetime.today().strftime('%H-%M-%S_%d-%m-%Y')
        tx_id = self.filename
        self.filename = f'{self.filename}-fb-{postfix}:{locations["FTP"]}'
        self.output_type = OutputType.FEEDBACK
        self._from_survey(survey_dict)
        # reset the transaction id to the filename
        self.tx_id = tx_id

    def set_comments(self):
        self.filename = f'{self.filename}:{locations["FTP"]}'
        self.output_type = OutputType.COMMENTS
        self.tx_id = self.filename

    def set_seft(self, meta_dict: dict):
        self.filename = f'{self.filename}:{locations["FTP"]}'
        self.output_type = OutputType.SEFT
        self.tx_id = meta_dict['tx_id']
        self.survey_id = meta_dict['survey_id']
        self.period = meta_dict['period']
        self.ru_ref = meta_dict['ru_ref']
        self.md5sum = meta_dict['md5sum']
        self.sizeBytes = meta_dict['sizeBytes']

    def get_description(self) -> str:
        if self.output_type == OutputType.COMMENTS:
            return "Comments.zip"
        else:
            response_type = {OutputType.DAP: 'survey',
                             OutputType.LEGACY: 'survey',
                             OutputType.HYBRID: 'survey',
                             OutputType.FEEDBACK: 'feedback',
                             OutputType.SEFT: 'seft'}.get(self.output_type)
            return f"{self.survey_id} {response_type} response for period {self.period} sample unit {self.ru_ref}"


class MetaWrapperV2(MetaWrapper):

    def _from_survey(self, survey_dict: dict):
        self.tx_id = _get_field(survey_dict, 'tx_id')
        self.survey_id = _get_field(survey_dict, 'survey_metadata', 'survey_id')
        self.period = _get_field(survey_dict, 'survey_metadata', 'period_id')
        self.ru_ref = _get_field(survey_dict, 'survey_metadata', 'ru_ref')


class MetaWrapperAdhoc(MetaWrapper):
    """MetaWrapper for adhoc surveys

    The Winter Surveillance Survey is split into 2 surveys
    (738 fuis, and 739 wcis) however NIFI has only one flow for each.
    Therefore, submissions for fuis need to be changed to survey id 739.
    To allow the end users to distinguish between the 2, the filename is
    prefixed with the original survey id.
    """
    def __init__(self, filename: str):
        super().__init__(filename)

    def _from_survey(self, survey_dict: dict):
        self.tx_id = _get_field(survey_dict, 'tx_id')
        survey_id = _get_field(survey_dict, 'survey_metadata', 'survey_id')
        if self.output_type == OutputType.DAP:
            if survey_id == "739":
                self.filename = f'739-{self.filename}'
            elif survey_id == "738":
                self.filename = f'738-{self.filename}'
        self.survey_id = survey_id
        self.period = None
        self.ru_ref = None

    def get_description(self) -> str:
        if self.output_type == OutputType.FEEDBACK:
            return f"{self.survey_id} feedback response for adhoc survey"
        return f"{self.survey_id} survey response for adhoc survey"
