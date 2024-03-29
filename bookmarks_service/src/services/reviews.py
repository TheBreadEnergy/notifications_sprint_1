from abc import ABC, abstractmethod
from uuid import UUID

from src.core.pagination import PaginatedPage
from src.models.review import Review
from src.repositories.reviews import ReviewsRepositoryABC
from src.schema.likes import LikeType
from src.schema.reviews import ReviewCreateDto
from src.schema.user import Roles, UserDto, UserMeta


class ReviewsServiceABC(ABC):
    @abstractmethod
    async def get_reviews(
        self, *, film_id: UUID | None = None, user_id: UUID | None = None
    ) -> PaginatedPage[Review]:
        ...

    @abstractmethod
    async def get_review(self, *, review_id: UUID) -> Review | None:
        ...

    @abstractmethod
    async def create_review(self, *, data: ReviewCreateDto, user: UserMeta) -> Review:
        ...

    @abstractmethod
    async def update_review(
        self, review_id: UUID, user_id: UUID, review_text: str
    ) -> Review | None:
        ...

    @abstractmethod
    async def add_like_to_review(
        self, *, review_id: UUID, user: UserMeta, like_type: LikeType
    ) -> Review | None:
        ...

    @abstractmethod
    async def remove_like_from_review(
        self, *, review_id: UUID, user: UserMeta
    ) -> Review | None:
        ...

    @abstractmethod
    async def delete_review(self, *, review_id: UUID, user: UserDto) -> None:
        ...

    @abstractmethod
    async def delete_review_like(self, *, review_id: UUID, user: UserDto) -> Review:
        ...


def check_admin_role(user: UserDto) -> bool:
    role_names = [role.name for role in user.roles]
    return Roles.ADMIN in role_names or Roles.SUPER_ADMIN in role_names


class ReviewsService(ReviewsServiceABC):
    def __init__(self, repo: ReviewsRepositoryABC):
        self._repo = repo

    async def get_reviews(
        self, *, film_id: UUID | None = None, user_id: UUID | None = None
    ) -> PaginatedPage[Review]:
        return await self._repo.search(film_id=film_id, user_id=user_id)

    async def get_review(self, *, review_id: UUID) -> Review | None:
        return await self._repo.get(entity_id=id)

    async def create_review(self, *, data: ReviewCreateDto, user: UserMeta) -> Review:
        review = Review(user=user, film=data.film, text=data.text)
        return await self._repo.insert(entity=review)

    async def update_review(
        self, review_id: UUID, user_id: UUID, review_text: str
    ) -> Review | None:
        return await self._repo.update_review_text(
            review_id=review_id, text=review_text, user_id=user_id
        )

    async def add_like_to_review(
        self, *, review_id: UUID, user: UserMeta, like_type: LikeType
    ) -> Review | None:
        return await self._repo.add_like_to_review(
            review_id=review_id, user=user, like_type=like_type
        )

    async def remove_like_from_review(
        self, *, review_id: UUID, user: UserMeta
    ) -> Review | None:
        review = await self._repo.delete_like_from_review(
            review_id=review_id, user_id=user.user_id
        )
        return review

    async def delete_review(self, *, review_id: UUID, user: UserDto) -> None:
        if check_admin_role(user) or await self._check_ownership(
            review_id=review_id, user_id=user.id
        ):
            await self._repo.delete(entity_id=id)

    async def delete_review_like(self, *, review_id: UUID, user: UserDto) -> Review:
        return await self._repo.delete_like_from_review(review_id, user_id=user.id)

    async def _check_ownership(self, review_id: UUID, user_id: UUID) -> bool:
        entity = await self._repo.get(entity_id=review_id)
        return entity and entity.user.id == user_id
