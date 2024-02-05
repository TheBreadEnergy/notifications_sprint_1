from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.film import Film, Films
from src.services.bearer import security_jwt
from src.services.film import FilmServiceABC

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=Film,
    description="Вывод подробной информации о запрашиваемом кинопроизведении",
    tags=["Фильмы"],
    summary="Подробная информация о кинопроизведении",
    response_description="Информация о кинопроизведении",
)
async def film_details(
    film_id: UUID,
    film_service: FilmServiceABC = Depends(),
    user: Annotated[dict, Depends(security_jwt)] = None,
) -> Film:
    film = await film_service.get(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return film


# Add descriptions
# Add new method /search with the same query params
@router.get(
    "/search/",
    response_model=list[Films],
    description="Поиск подробной информации о кинопроизведениях",
    tags=["Фильмы"],
    summary="Поиск информации о кинопроизведениях",
    response_description="Информация о кинопроизведении",
)
async def search_films(
    query: str,
    film_service: FilmServiceABC = Depends(),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=40),
    user: Annotated[dict, Depends(security_jwt)] = None,
) -> list[Films]:
    films = await film_service.search(title=query, page=page, size=size)
    if not films:
        return list()
    return films


@router.get(
    "/",
    response_model=list[Films],
    description="Вывод подробной информации о запрашиваемых кинопроизведениях",
    tags=["Фильмы"],
    summary="Подробная информация о кинопроизведениях",
    response_description="Информация о кинопроизведениях",
)
async def list_films(
    sort=None,
    id_film: UUID = None,
    genre: str = None,
    actor_id: str = None,
    writer_id: str = None,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=40),
    film_service: FilmServiceABC = Depends(),
    user: Annotated[dict, Depends(security_jwt)] = None,
) -> list[Films]:
    data_filter = {}
    if id_film:
        data_filter["id"] = id_film
    if genre:
        data_filter["genres"] = genre
    if actor_id:
        data_filter["actors"] = actor_id
    if writer_id:
        data_filter["writers"] = writer_id

    films = await film_service.gets(
        sort=sort, data_filter=data_filter, page=page, size=size
    )
    if not films:
        return list()
    return films
