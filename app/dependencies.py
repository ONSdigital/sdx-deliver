from fastapi import Depends
from sdx_base.services.pubsub import PubsubService
from sdx_base.services.storage import StorageService

from app.definitions.message_builder import MessageBuilderBase
from app.definitions.submission_type_mapper import SubmissionTypeMapperBase
from app.deliver import Deliver
from app.services.encryption import EncryptionService
from app.services.location import LocationKeyLookup
from app.services.message_builder import MessageBuilder
from app.services.publish import PublishService
from app.services.submission_type_mapper import SubmissionTypeMapper
from app.services.zip import ZipService
from app.settings import Settings, get_instance


def get_settings() -> Settings:
    return get_instance()


def get_encryption_service() -> EncryptionService:
    settings: Settings = Depends(get_settings)
    return EncryptionService(settings)


def get_location_service() -> LocationKeyLookup:
    settings: Settings = Depends(get_settings)
    return LocationKeyLookup(settings)


def get_submission_type_mapper() -> SubmissionTypeMapperBase:
    key_lookup: LocationKeyLookup = Depends(get_location_service)
    return SubmissionTypeMapper(key_lookup)


def get_message_builder() -> MessageBuilderBase:
    settings: Settings = Depends(get_settings)
    submission_mapper: SubmissionTypeMapperBase = Depends(get_submission_type_mapper)
    return MessageBuilder(submission_mapper, data_sensitivity=settings.data_sensitivity)


def get_zip_service() -> ZipService:
    return ZipService()


def get_publish_service() -> PublishService:
    settings: Settings = Depends(get_settings)
    return PublishService(PubsubService(), dap_topic_id=settings.dap_topic_id)


def get_storage_service() -> StorageService:
    return StorageService()


def get_deliver_service() -> Deliver:
    message_builder: MessageBuilderBase = Depends(get_message_builder)
    encrypter: EncryptionService = Depends(get_encryption_service)
    publisher: PublishService = Depends(get_publish_service)
    storer: StorageService = Depends(get_storage_service)
    zipper: ZipService = Depends(get_zip_service)
    settings: Settings = Depends(get_settings)
    return Deliver(
        message_builder=message_builder,
        encrypter=encrypter,
        publisher=publisher,
        bucket=settings.bucket_name,
        storer=storer,
        zipper=zipper
    )
