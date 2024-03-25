from abc import ABC, abstractmethod
from uuid import UUID

from src.core.pagination import PaginatedPage
from src.models.review import Review
from src.repositories.reviews import ReviewsRepositoryABC
from src.schema.likes import LikeType
from src.schema.reviews import ReviewCreateDto
from src.schema.user import UserMeta


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
    async def update_review(self, review_id: UUID, review_text: str) -> Review | None:
        ...

    @abstractmethod
    async def add_like_to_review(
        self, *, review_id: UUID, user: UserMeta, like_type: LikeType
    ) -> Review:
        ...

    @abstractmethod
    async def remove_like_from_review(
        self, *, review_id: UUID, user: UserMeta
    ) -> Review:
        ...

    @abstractmethod
    async def delete_review(self, *, review_id: UUID) -> None:
        ...


class ReviewsService(ReviewsServiceABC):
    def __init__(self, repo: ReviewsRepositoryABC):
        self._repo = repo

    async def get_reviews(
        self, *, film_id: UUID | None = None, user_id: UUID | None = None
    ) -> PaginatedPage[Review]:
        return await self.get_reviews(film_id=film_id, user_id=user_id)

    async def get_review(self, *, review_id: UUID) -> Review | None:
        return await self._repo.get(entity_id=id)

    async def create_review(self, *, data: ReviewCreateDto, user: UserMeta) -> Review:
        review = Review(user=user, film=data.film, text=data.text)
        return await self._repo.insert(entity=review)

    async def update_review(self, review_id: UUID, review_text: str) -> Review | None:
        return await self._repo.update_review_text(
            review_id=review_id, text=review_text
        )

    async def add_like_to_review(
        self, *, review_id: UUID, user: UserMeta, like_type: LikeType
    ) -> Review:
        await self._repo.delete_like_from_review(
            review_id=review_id, user_id=user.user_id
        )
        return await self._repo.add_like_to_review(
            review_id=review_id, user=user, like_type=like_type
        )

    async def remove_like_from_review(
        self, *, review_id: UUID, user: UserMeta
    ) -> Review:
        review = await self._repo.delete_like_from_review(
            review_id=review_id, user_id=user.user_id
        )
        return review

    async def delete_review(self, *, review_id: UUID) -> None:
        await self._repo.delete(entity_id=id)
