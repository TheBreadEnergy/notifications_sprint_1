from abc import ABC, abstractmethod

from aiohttp import ClientSession
from fastapi import UploadFile
from miniopy_async import Minio
from src.schemas.file import FileUploadDto
from starlette.responses import StreamingResponse


class Storage(ABC):
    @abstractmethod
    def save(self, *args, **kwargs) -> FileUploadDto:
        ...

    @abstractmethod
    def get_file(self, *args, **kwargs) -> StreamingResponse:
        ...


class MinioStorage(Storage):
    def __init__(self, minio_client: Minio, session_client: ClientSession):
        self._minio = minio_client
        self._session_client = session_client

    async def save(self, *, file: UploadFile, bucket: str, path: str) -> FileUploadDto:
        response = await self._minio.put_object(
            bucket_name=bucket,
            object_name=path,
            data=file,
            length=file.size,
            part_size=10 * 1024 * 1024,
        )
        file_response = FileUploadDto(
            url=response.location,
            bucket_name=response.bucket_name,
            object_name=response.object_name,
            version_id=response.version_id,
        )
        return file_response

    async def get_file(
        self, *, bucket: str, path: str, file_type: str, filename: str
    ) -> StreamingResponse:
        response = await self._minio.get_object(bucket, path, self._session_client)

        async def s3_stream():
            async for chunk in response.content.iter_chunked(32 * 1024):
                yield chunk

        return StreamingResponse(content=s3_stream(), media_type=file_type)
