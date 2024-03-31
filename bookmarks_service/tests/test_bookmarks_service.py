import uuid
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from src.schema.user import UserDto
from src.services.bookmarks import BookmarkService

faker = Faker()


@pytest.mark.asyncio
async def test_get_bookmarks_for_user():
    mock_repository = AsyncMock()
    service = BookmarkService(repo=mock_repository)
    user_id = uuid.uuid4()
    await service.get_bookmarks_for_user(user_id=user_id)
    mock_repository.search.assert_called_once_with(user_id=user_id)


@pytest.mark.asyncio
async def test_delete_bookmark():
    mock_repository = AsyncMock()
    service = BookmarkService(repo=mock_repository)
    bookmark_id = uuid.uuid4()
    user = UserDto(
        id=uuid.uuid4(),
        login=faker.word(),
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        roles=[],
    )
    await service.delete_bookmark(bookmark_id=bookmark_id, user=user)
    mock_repository.delete.assert_called_once_with(
        entity_id=bookmark_id, user_id=user.id
    )


@pytest.mark.asyncio
async def test_delete_bookmarks_for_user():
    mock_repository = AsyncMock()
    service = BookmarkService(repo=mock_repository)
    user_id = uuid.uuid4()
    await service.delete_all_bookmarks_for_user(user_id=user_id)
    mock_repository.delete.assert_called_once_with(user_id=user_id)
