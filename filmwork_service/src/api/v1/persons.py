from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.person import Person
from src.services.bearer import security_jwt
from src.services.persons import PersonServiceABC

router = APIRouter()


@router.get(
    "/{person_id}",
    response_model=Person,
    description="Вывод подробной информации о запрашиваемом персоне",
    tags=["Персоны"],
    summary="Подробная информация о персоне",
    response_description="Информация о персоне",
)
async def person_details(
    person_id: UUID,
    person_service: PersonServiceABC = Depends(),
    user: Annotated[dict, Depends(security_jwt)] = None,
) -> Person:
    person = await person_service.get(person_id=person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")

    return person


@router.get(
    "/search/",
    response_model=list[Person],
    description="Поиск подробной информации о запрашиваемых персонах",
    tags=["Персоны"],
    summary="Поиск информации о запрашиваемых персонах",
    response_description="Информация о запрашиваемых персонах",
)
async def search_person(
    query: str,
    person_service: PersonServiceABC = Depends(),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=40),
    user: Annotated[dict, Depends(security_jwt)] = None,
) -> list[Person]:
    persons = await person_service.search(name=query, page=page, size=size)
    if not persons:
        return list()
    return persons


@router.get(
    "/",
    response_model=list[Person],
    description="Вывод подробной информации о запрашиваемых персонах",
    tags=["Персоны"],
    summary="Подробная информация о персонах",
    response_description="Информация о персонах",
)
async def list_persons(
    sort: str = Query(default="asc", regex="^(asc|desc)$"),
    id_person: UUID = None,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=40),
    person_service: PersonServiceABC = Depends(),
    user: Annotated[dict, Depends(security_jwt)] = None,
) -> list[Person]:
    data_filter = {}
    if id_person:
        data_filter["id"] = id_person
    persons = await person_service.gets(
        sort=sort, data_filter=data_filter, page=page, size=size
    )
    if not persons:
        return list()
    return persons
