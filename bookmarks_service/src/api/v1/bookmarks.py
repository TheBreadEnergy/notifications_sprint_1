from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from src.core.pagination import PaginatedPage
from src.models import Bookmark
from src.schema.bookmarks import BookmarkCreateDto, BookmarkDto
from src.schema.user import UserDto
from src.services.bearer import security_jwt
from src.services.bookmarks import BookmarkServiceABC

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedPage[BookmarkDto],
    response_description="Список закладок пользователя",
    description="Выдача списка закладок пользователя",
    summary="Выдача списка закладок пользователя",
    tags=["Закладки"],
)
async def get_bookmarks(
    bookmark_service: BookmarkServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
) -> PaginatedPage[Bookmark]:
    return await bookmark_service.get_bookmarks_for_user(user_id=user.id)


@router.post(
    "/",
    response_model=BookmarkDto,
    response_description="Созданная закладка для пользователя",
    tags=["Закладки"],
)
async def create_bookmark(
    data: BookmarkCreateDto,
    bookmark_service: BookmarkServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
) -> Bookmark:
    return await bookmark_service.create_bookmark(data=data, user=user)


@router.delete(
    "/all",
    summary="Удалить все свои закладки",
    description="Удалить все свои закладки",
    tags=["Закладки"],
)
async def delete_all_bookmarks(
    bookmark_service: BookmarkServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
):
    return await bookmark_service.delete_all_bookmarks_for_user(user_id=user.id)


@router.delete(
    "/{bookmark_id}",
    summary="Удаляет выбранную закладку",
    description="Удаляет выбранную закладку",
    tags=["Закладки"],
)
async def delete_bookmark(
    bookmark_id: UUID,
    bookmark_service: BookmarkServiceABC = Depends(),
    user: Annotated[UserDto, Depends(security_jwt)] = None,
):
    return await bookmark_service.delete_bookmark(bookmark_id=bookmark_id, user=user)
