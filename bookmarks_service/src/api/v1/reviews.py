from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from src.core.pagination import PaginatedPage
from src.models import Review
from src.schema.reviews import (
    ReviewCreateDto,
    ReviewDto,
    ReviewLikeCreateDto,
    ReviewUpdateDto,
)
from src.schema.user import UserDto
from src.services.bearer import security_jwt
from src.services.reviews import ReviewsServiceABC

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedPage[ReviewDto],
    summary="Выдача страницы с отзывами пользователя",
    description="Выдача страницы с отзывами пользователя",
    response_description="Страница с отзывами пользователя",
    tags=["Отзывы"],
)
async def get_user_reviews(
    review_service: ReviewsServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
) -> PaginatedPage[Review]:
    return await review_service.get_reviews(user_id=user.id)


@router.get(
    "/film/{film_id}",
    response_model=PaginatedPage[ReviewDto],
    summary="Выдача страницы с отзывами на конкретный фильм",
    description="Выдача страницы с отзывами на конкретный фильм",
    response_description="Страница с отзывами пользователей о фильме",
    tags=["Отзывы"],
)
async def get_film_reviews(
    film_id: UUID,
    review_service: ReviewsServiceABC = Depends(),
) -> PaginatedPage[ReviewDto]:
    return await review_service.get_reviews(film_id=film_id)


@router.get(
    "/{review_id}",
    response_model=ReviewDto,
    summary="Выдача конкретного отзыва",
    description="Выдача конкретного отзыва по заданному id",
    tags=["Отзывы"],
    response_description="Сведения об отзыве",
)
async def get_reviews(
    review_id: UUID, review_service: ReviewsServiceABC = Depends()
) -> Review:
    review = await review_service.get_review(review_id=review_id)
    if not review:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Отзыв не найден")
    return review


@router.post(
    "/",
    response_model=ReviewDto,
    summary="Добавление отзыва",
    description="Добавление отзыва на фильм",
    response_description="Сведения об отзыве",
    tags=["Отзывы"],
)
async def create_review(
    data: ReviewCreateDto,
    review_service: ReviewsServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
) -> Review:
    return await review_service.create_review(data=data, user=user)


@router.post(
    "/{review_id}/likes",
    response_model=ReviewDto,
    summary="Добавление лайка / дизлайка на комментарий",
    description="Добавление лайка / дизлайка на комментарий",
    tags=["Отзывы"],
    response_description="Сведения об отзыве",
)
async def add_like_to_review(
    review_id: UUID,
    data: ReviewLikeCreateDto,
    review_service: ReviewsServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
) -> Review:
    review = await review_service.add_like_to_review(
        review_id=review_id, like_type=data.like_type, user=user
    )
    if not review:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Отзыв не найден")
    return review


@router.put(
    "/{review_id}",
    response_model=ReviewDto,
    summary="Редактирование текста отзыва",
    description="Редактирование текста отзыва",
    tags=["Отзывы"],
    response_description="Сведения об отзыве",
)
async def update_review(
    review_id: UUID,
    data: ReviewUpdateDto,
    review_service: ReviewsServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
) -> Review:
    review = await review_service.update_review(
        review_id=review_id, user_id=user.id, review_text=data.text
    )
    if not review:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Не найдено отзыва у текущего пользователя",
        )
    return review


@router.delete(
    "/{review_id}",
    summary="Удалить отзыв пользователя",
    description="Удалить отзыв пользователя",
    tags=["Отзывы"],
)
async def delete_review(
    review_id: UUID,
    review_service: ReviewsServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
):
    return await review_service.delete_review(review_id=review_id, user=user)


@router.delete(
    "/{review_id}/likes",
    summary="Удалить отзыв пользователя",
    description="Удалить отзыв пользователя",
    tags=["Отзывы"],
)
async def delete_review_like(
    review_id: UUID,
    review_service: ReviewsServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
):
    return await review_service.delete_review_like(review_id=review_id, user=user)
