from abc import ABC, abstractmethod


class FileNameMapperBase(ABC):

    @abstractmethod
    def get_output_type(self, filename: str, submission_type: str) -> str:
        pass


