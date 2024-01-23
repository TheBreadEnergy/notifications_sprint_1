from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.genre import Genre
from src.services.genres import GenreServiceABC

router = APIRouter()


@router.get(
    "/{genre_id}",
    response_model=Genre,
    description="Вывод подробной информации о запрашиваемом жанре",
    tags=["Жанры"],
    summary="Подробная информация о жанре",
    response_description="Информация о жанре",
)
async def genre_details(
    genre_id: UUID, genre_service: GenreServiceABC = Depends()
) -> Genre:
    genre = await genre_service.get(genre_id=genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")

    return genre


@router.get(
    "/search/",
    response_model=list[Genre],
    description="Поиск подробной информации о запрашиваемых жанрах",
    tags=["Жанры"],
    summary="Поиск информации о запрашиваемых жанрах",
    response_description="Информация о запрашиваемых жанрах",
)
async def search_genre(
    query: str,
    genre_service: GenreServiceABC = Depends(),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=40),
) -> list[Genre]:
    genres = await genre_service.search(name=query, page=page, size=size)
    if not genres:
        return list()
    return genres


@router.get(
    "/",
    response_model=list[Genre],
    description="Вывод подробной информации о запрашиваемых жанрах",
    tags=["Жанры"],
    summary="Подробная информация о жанрах",
    response_description="Информация о жанрах",
)
async def list_genres(
    sort: str = Query(default="asc", regex="^(asc|desc)$"),
    id_genre: UUID = None,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=40),
    genre_service: GenreServiceABC = Depends(),
) -> list[Genre]:
    data_filter = {}
    if id_genre:
        data_filter["id"] = id_genre
    genres = await genre_service.gets(
        sort=sort, data_filter=data_filter, page=page, size=size
    )
    if not genres:
        return list()
    return genres
