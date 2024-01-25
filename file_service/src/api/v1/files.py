from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from src.core.config import settings
from src.schemas.file import FileBaseDto, FileResponseDto
from src.services.file import FileMetaServiceABC, FileServiceABC
from starlette.responses import StreamingResponse

router = APIRouter()


@router.get(
    "/",
    response_model=list[FileBaseDto],
    description="Вывод списка загруженных фильмов",
    tags=["Фильмы"],
    summary="Краткая информация о всех загруженных фильмах с постраничным выводом",
    response_description="Информация о файлах",
)
async def list_files_meta(
    file_repository: FileMetaServiceABC = Depends(),
    skip: Annotated[int, Query(description="Items to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
):
    films = await file_repository.get_files(skip=skip, limit=limit)
    if not films:
        return list()
    return films


@router.get(
    "/{short_name}",
    response_model=FileResponseDto,
    description="Вывод подробной информации о запрашиваемом файле фильма",
    tags=["Фильмы"],
    summary="Подробная информация о файле",
    response_description="Информация о файле",
)
async def get_file_meta(
    short_name: str, file_repository: FileMetaServiceABC = Depends()
) -> FileResponseDto:
    film = await file_repository.get_file_by_name(name=short_name)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="file meta not found"
        )
    return film


@router.get(
    "/download-stream/{short_name}",
    response_model=FileResponseDto,
    description="Скачивание файла из репозитория по его имени",
    tags=["Фильмы"],
    summary="Скачивание файла из репозитория по его имени",
    response_description="Скачивание файла из репозитория по его имени",
)
async def download_file(
    short_name: str, file_service: FileServiceABC = Depends()
) -> StreamingResponse:
    stream = await file_service.download_file(settings.s3_bucket, short_name)
    if not stream:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="file not found")
    return stream


@router.post(
    "/",
    response_model=FileResponseDto,
    description="Загрузка файла в хранилище",
    tags=["Фильмы"],
    summary="Загрузка файла в хранилище",
    response_description="Загрузка файла в хранилище",
)
async def upload_file(
    file: UploadFile, file_service: FileServiceABC = Depends()
) -> FileResponseDto:
    response = await file_service.upload_file(settings.s3_bucket, file)
    return response
