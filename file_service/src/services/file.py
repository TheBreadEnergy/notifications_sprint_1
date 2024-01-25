from abc import ABC, abstractmethod

import shortuuid
from fastapi import UploadFile
from src.models.file import File
from src.schemas.file import FileCreateDto, FileUploadDto
from src.services.base import PostgresRepository
from src.storage.base import Storage
from starlette.responses import StreamingResponse


class FileRepository(PostgresRepository[File, FileCreateDto]):
    ...


class FileServiceABC(ABC):
    @abstractmethod
    def upload_file(self, bucket_name: str, file: UploadFile) -> File:
        ...

    @abstractmethod
    def download_file(
        self, bucket_name: str, short_name: str
    ) -> StreamingResponse | None:
        ...


class FileMetaServiceABC(ABC):
    @abstractmethod
    def get_files(self, *, skip: int, limit: int) -> list[File]:
        ...

    @abstractmethod
    def get_file_by_name(self, *, name: str) -> File:
        ...


class FileService(FileServiceABC):
    def __init__(
        self, repository: PostgresRepository[File, FileCreateDto], storage: Storage
    ):
        self._repository = repository
        self._storage = storage

    async def upload_file(self, bucket_name: str, file: UploadFile) -> File:
        short_name = shortuuid.uuid()
        _: FileUploadDto = await self._storage.save(
            file=file, bucket=bucket_name, path=short_name
        )
        file_meta = FileCreateDto(
            filename=file.filename,
            short_name=short_name,
            size=file.size,
            file_type=file.content_type,
            url=f"{file.filename}",
        )
        file_response = await self._repository.insert(obj=file_meta)
        return file_response

    async def download_file(self, bucket_name: str, short_name: str):
        file_meta: File = await self._repository.get_by_name(short_name=short_name)
        if not file_meta:
            return None

        return await self._storage.get_file(
            bucket=bucket_name,
            path=file_meta.short_name,
            filename=file_meta.filename,
            file_type=file_meta.file_type,
        )


class FileMetaService(FileMetaServiceABC):
    def __init__(self, repository: FileRepository):
        self._repository = repository

    async def get_files(self, *, skip: int, limit: int) -> list[File]:
        return await self._repository.gets(skip=skip, limit=limit)

    async def get_file_by_name(self, *, name: str) -> File:
        return await self._repository.get_by_name(short_name=name)
