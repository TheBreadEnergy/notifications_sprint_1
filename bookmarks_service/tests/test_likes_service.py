import uuid
from unittest.mock import AsyncMock

import pytest
from src.services.film_likes import FilmLikeService


@pytest.mark.asyncio
async def test_get_likes_for_film():
    mock_repository = AsyncMock()
    reviews_service = FilmLikeService(repo=mock_repository)
    film_id = uuid.uuid4()
    await reviews_service.get_film_likes(film_id=film_id)
    mock_repository.search.assert_called_once_with(film_id=film_id, user_id=None)


@pytest.mark.asyncio
async def test_get_likes_for_user():
    mock_repository = AsyncMock()
    reviews_service = FilmLikeService(repo=mock_repository)
    user_id = uuid.uuid4()
    await reviews_service.get_film_likes(user_id=user_id)
    mock_repository.search.assert_called_once_with(film_id=None, user_id=user_id)
