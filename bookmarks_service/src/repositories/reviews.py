from abc import ABC, abstractmethod
from uuid import UUID

from beanie.odm.operators.find.comparison import Eq
from beanie.odm.operators.update.array import AddToSet, Pull
from beanie.odm.operators.update.general import Set
from src.models.review import Review
from src.repositories.base import MongoRepository, RepositoryABC
from src.schema.likes import LikeType, ReviewLikeMeta
from src.schema.user import UserMeta


class ReviewsRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    async def update_review_text(
        self, review_id: UUID, user_id: UUID, text: str
    ) -> Review | None:
        ...

    @abstractmethod
    async def add_like_to_review(
        self, review_id: UUID, user: UserMeta, like_type: LikeType
    ) -> Review | None:
        ...

    @abstractmethod
    async def delete_like_from_review(
        self, review_id: UUID, user_id: UUID
    ) -> Review | None:
        ...


class MongoReviewsRepository(MongoRepository[Review], ReviewsRepositoryABC):
    def __init__(self):
        super().__init__(model=Review)

    async def update_review_text(
        self, review_id: UUID, user_id: UUID, text: str
    ) -> Review | None:
        review = await Review.find_one(
            Review.id == review_id and Review.user.id == user_id
        )
        if not review:
            return None
        await review.update(Set({Review.text: text}))
        return review

    async def add_like_to_review(
        self, review_id: UUID, user: UserMeta, like_type: LikeType
    ) -> Review | None:
        review = await Review.find_one(Review.id == review_id)
        if not review:
            return None
        await review.update(
            AddToSet({Review.likes: ReviewLikeMeta(type=like_type, user=user)})
        )
        return review

    async def delete_like_from_review(
        self, review_id: UUID, user_id: UUID
    ) -> Review | None:
        review = await Review.find_one(Review.id == review_id)
        if not review:
            return None
        await review.update(Pull(Eq(ReviewLikeMeta.user.id, user_id)))
        return review
