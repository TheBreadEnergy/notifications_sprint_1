from functools import cache

from src.dependencies.registrator import add_factory_to_mapper
from src.repositories.reviews import MongoReviewsRepository
from src.services.reviews import ReviewsService, ReviewsServiceABC


@add_factory_to_mapper(ReviewsServiceABC)
@cache
def create_review_service() -> ReviewsService:
    return ReviewsService(repo=MongoReviewsRepository())
