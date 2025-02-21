from abc import ABC, abstractmethod


class FileNameMapperBase(ABC):

    @abstractmethod
    def get_output_type(self, filename: str) -> str:
        pass


class FileExtensionMapper(FileNameMapperBase):

    def get_output_type(self, filename: str) -> str:
        split_string = filename.split(".")
        if len(split_string) == 1:
            return "pck"
        extension = split_string[1]
        if extension == "jpg":
            return "image"
        if extension == "csv":
            return "index"
        if extension == "dat":
            return "receipt"
        return "json"
