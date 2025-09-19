from fastapi import Depends
from sdx_base.services.pubsub import PubsubService
from sdx_base.services.storage import StorageService

from app.definitions.encryption import EncryptionBase
from app.definitions.gcp import GcpBase
from app.definitions.location import LocationBase
from app.definitions.message_builder import MessageBuilderBase
from app.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.definitions.zip import ZipBase
from app.deliver import Deliver
from app.services.encryption import EncryptionService
from app.services.gcp import GcpService
from app.services.location import LocationService
from app.services.mapper import SubmissionTypeMapper
from app.services.message_builder import MessageBuilder
from app.services.zip import ZipService
from app.settings import Settings, get_instance


def get_settings() -> Settings:
    return get_instance()


def get_encryption_service() -> EncryptionService:
    settings: Settings = Depends(get_settings)
    return EncryptionService(settings)


def get_location_service() -> LocationService:
    settings: Settings = Depends(get_settings)
    return LocationService(settings)


def get_mapper_service() -> SubmissionTypeMapperBase:
    location_service: LocationBase = Depends(get_location_service)
    return SubmissionTypeMapper(location_service)


def get_message_builder() -> MessageBuilderBase:
    settings: Settings = Depends(get_settings)
    submission_mapper: SubmissionTypeMapperBase = Depends(get_mapper_service)
    return MessageBuilder(submission_mapper,
                          data_sensitivity=settings.data_sensitivity)


def get_zip_service() -> ZipService:
    return ZipService()


def get_gcp_service() -> GcpService:
    settings: Settings = Depends(get_settings)
    return GcpService(PubsubService(), StorageService(), settings)


def get_deliver_service() -> Deliver:
    message_builder: MessageBuilderBase = Depends(get_message_builder)
    encrypter: EncryptionBase = Depends(get_encryption_service)
    gcp: GcpBase = Depends(get_gcp_service)
    zipper: ZipBase = Depends(get_zip_service)
    return Deliver(
        message_builder=message_builder,
        encrypter=encrypter,
        gcp=gcp,
        zipper=zipper
    )
