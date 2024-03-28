from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from src.core.pagination import PaginatedPage
from src.models import FilmLike
from src.schema.likes import FilmLikeCreateDto, FilmLikeDto
from src.schema.user import UserDto
from src.services.bearer import security_jwt
from src.services.film_likes import FilmLikeServiceABC

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedPage[FilmLikeDto],
    summary="Вывод страницы лайков "
    "/ дизлайков поставленных авторизированным пользователем",
    description="Вывод страницы лайков "
    "/ дизлайков поставленных авторизированным пользователем",
    response_description="Страница с лайками / дизлайками",
    tags=["Лайки / Дизлайки"],
)
async def get_film_likes(
    like_service: FilmLikeServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
) -> PaginatedPage[FilmLike]:
    return await like_service.get_film_likes(user_id=user.id)


@router.get(
    "/{film_id}",
    response_model=PaginatedPage[FilmLikeDto],
    summary="Вывод страницы лайков "
    "/ дизлайков поставленных авторизированным пользователем",
    description="Вывод страницы лайков "
    "/ дизлайков поставленных авторизированным пользователем",
    response_description="Страница с лайками / дизлайками",
    tags=["Лайки / Дизлайки"],
)
async def get_film_likes_for_film(
    film_id: UUID,
    like_service: FilmLikeServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,  # noqa F401
) -> PaginatedPage[FilmLike]:
    return await like_service.get_film_likes(film_id=film_id)


@router.post(
    "/",
    response_model=FilmLikeDto,
    summary="Поставить лайк выбранному фильму",
    description="Поставить лайк выбранному фильму",
    tags=["Лайки / Дизлайки"],
)
async def create_film_like(
    data: FilmLikeCreateDto,
    like_service: FilmLikeServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
) -> FilmLike:
    return await like_service.create_film_like(
        film=data.film, like_type=data.like_type, user=user
    )


@router.delete(
    "/{film_id}",
    summary="Удалить лайк у выбранного фильма",
    description="Удалить лайк у выбранного фильма",
    tags=["Лайки / Дизлайки"],
)
async def delete_film_like(
    film_id: UUID,
    like_service: FilmLikeServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
):
    await like_service.delete_film_like(film_id=film_id, user_id=user.id)
