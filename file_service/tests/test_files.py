import random
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from fastapi import UploadFile
from src.models.file import File
from src.services.file import FileMetaService, FileService

fake = Faker()

mime_types = ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/svg+xml"]


def fake_file():
    file_mime_type = random.choice(mime_types)
    return File(
        id=fake.uuid4(),
        filename=fake.file_name(category=None, extension=file_mime_type.split("/")[-1]),
        short_name=fake.uuid4(),
        size=fake.random_number(digits=6),
        file_type=file_mime_type,
        url=fake.url(),
        created=fake.date_time_between(start_date="-5y", end_date="now"),
    )


@pytest.mark.asyncio
async def test_upload_file():
    mock_repository = AsyncMock()
    mock_storage = AsyncMock()
    mock_upload_file = AsyncMock(spec=UploadFile)

    file_mime_type = random.choice(mime_types)

    mock_upload_file.filename = fake.file_name(
        category=None, extension=file_mime_type.split("/")[-1]
    )
    mock_upload_file.content_type = file_mime_type
    mock_upload_file.size = fake.random_number(digits=6)

    file_service = FileService(repository=mock_repository, storage=mock_storage)

    await file_service.upload_file(bucket_name="test_bucket", file=mock_upload_file)

    mock_storage.save.assert_called_once()
    mock_repository.insert.assert_called_once()


@pytest.mark.asyncio
async def test_get_files():
    mock_repository = AsyncMock()
    list_files = [fake_file() for _ in range(0, random.randrange(1, 10))]
    mock_repository.gets.return_value = list_files

    file_meta_service = FileMetaService(repository=mock_repository)
    files = await file_meta_service.get_files(skip=0, limit=10)

    assert len(files) == len(list_files)
    mock_repository.gets.assert_called_once_with(skip=0, limit=10)


@pytest.mark.asyncio
async def test_get_file_by_name():
    mock_repository = AsyncMock()
    file_test = fake_file()
    mock_repository.get_by_name.return_value = file_test

    file_meta_service = FileMetaService(repository=mock_repository)
    file = await file_meta_service.get_file_by_name(name=file_test.filename)

    assert file.filename == file_test.filename
    mock_repository.get_by_name.assert_called_once_with(short_name=file_test.filename)
