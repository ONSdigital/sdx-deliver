from app.output_type import OutputType


locations = {
    "DAP": "dap",
    "FTP": "ftp",
    "HYBRID": "hybrid"
}


class MetaWrapper:

    """
    This class provides a common interface to the metadata associated with different types of survey submissions
    """

    def __init__(self, filename):
        self.filename = filename
        self.tx_id = None
        self.survey_id = None
        self.period = None
        self.ru_ref = None
        self.md5sum = None
        self.sizeBytes = 0
        self.output_type = None

    def _from_survey(self, survey_dict: dict):
        self.tx_id = survey_dict['tx_id']
        self.survey_id = survey_dict['survey_id']
        self.period = survey_dict['collection']['period']
        self.ru_ref = survey_dict['metadata']['ru_ref']

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
        self.filename = f'{self.filename}-feedback:{locations["FTP"]}'
        self.output_type = OutputType.FEEDBACK
        self._from_survey(survey_dict)

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
