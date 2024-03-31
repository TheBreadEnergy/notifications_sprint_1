import uuid
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from src.schema.likes import LikeType
from src.schema.user import RoleBase, Roles, UserDto, UserMeta
from src.services.reviews import ReviewsService

faker = Faker()


@pytest.mark.asyncio
async def test_get_film_reviews():
    mock_repository = AsyncMock()
    reviews_service = ReviewsService(repo=mock_repository)
    film_id = uuid.uuid4()
    await reviews_service.get_reviews(film_id=film_id)
    mock_repository.search.assert_called_once_with(film_id=film_id, user_id=None)


@pytest.mark.asyncio
async def test_get_user_reviews():
    mock_repository = AsyncMock()
    reviews_service = ReviewsService(repo=mock_repository)
    user_id = uuid.uuid4()
    await reviews_service.get_reviews(user_id=user_id)
    mock_repository.search.assert_called_once_with(user_id=user_id, film_id=None)


@pytest.mark.asyncio
async def test_get_review():
    mock_repository = AsyncMock()
    reviews_service = ReviewsService(repo=mock_repository)
    review_id = uuid.uuid4()
    await reviews_service.get_review(review_id=review_id)
    mock_repository.get.assert_called_once_with(entity_id=review_id)


@pytest.mark.asyncio
async def test_update_review():
    mock_repository = AsyncMock()
    reviews_service = ReviewsService(repo=mock_repository)
    review_id = uuid.uuid4()
    user_id = uuid.uuid4()
    text = faker.sentence()
    await reviews_service.update_review(
        review_id=review_id, user_id=user_id, review_text=text
    )
    mock_repository.update_review_text.assert_called_once_with(
        review_id=review_id, user_id=user_id, text=text
    )


@pytest.mark.asyncio
async def test_add_like_to_review():
    mock_repository = AsyncMock()
    reviews_service = ReviewsService(repo=mock_repository)
    review_id = uuid.uuid4()
    user = UserMeta(
        id=uuid.uuid4(),
        login=faker.word(),
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        roles=[],
    )
    await reviews_service.add_like_to_review(
        review_id=review_id, user=user, like_type=LikeType.like
    )
    mock_repository.add_like_to_review.assert_called_once_with(
        review_id=review_id, user=user, like_type=LikeType.like
    )


@pytest.mark.asyncio
async def test_remove_like_from_review():
    mock_repository = AsyncMock()
    reviews_service = ReviewsService(repo=mock_repository)
    review_id = uuid.uuid4()
    user = UserMeta(
        id=uuid.uuid4(),
        login=faker.word(),
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
    )
    await reviews_service.remove_like_from_review(review_id=review_id, user=user)
    mock_repository.delete_like_from_review.assert_called_once_with(
        review_id=review_id, user_id=user.id
    )


@pytest.mark.asyncio
async def test_delete_review_check_ownership():
    mock_repository = AsyncMock()
    reviews_service = ReviewsService(repo=mock_repository)
    reviews_service._check_ownership = AsyncMock(return_value=True)
    review_id = uuid.uuid4()
    user = UserDto(
        id=uuid.uuid4(),
        login=faker.word(),
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        roles=[],
    )
    await reviews_service.delete_review(review_id=review_id, user=user)
    reviews_service._check_ownership.assert_called_once_with(
        review_id=review_id, user_id=user.id
    )
    mock_repository.delete.assert_called_once_with(entity_id=review_id)


@pytest.mark.asyncio
async def test_delete_review_for_admin():
    mock_repository = AsyncMock()
    reviews_service = ReviewsService(repo=mock_repository)
    review_id = uuid.uuid4()
    user = UserDto(
        id=uuid.uuid4(),
        login=faker.word(),
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        roles=[RoleBase(id=uuid.uuid4(), name=Roles.ADMIN, description=None)],
    )
    await reviews_service.delete_review(review_id=review_id, user=user)
    mock_repository.delete.assert_called_once_with(entity_id=review_id)


@pytest.mark.asyncio
async def test_delete_review_cancel():
    mock_repository = AsyncMock()
    reviews_service = ReviewsService(repo=mock_repository)
    reviews_service._check_ownership = AsyncMock(return_value=False)
    review_id = uuid.uuid4()
    user = UserDto(
        id=uuid.uuid4(),
        login=faker.word(),
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        roles=[],
    )
    await reviews_service.delete_review(review_id=review_id, user=user)
    reviews_service._check_ownership.assert_called_once_with(
        review_id=review_id, user_id=user.id
    )
    mock_repository.delete.assert_not_called()
