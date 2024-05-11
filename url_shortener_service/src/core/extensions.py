from fastapi import Depends
from fastapi_limiter.depends import RateLimiter
from src.core.config import settings


def build_dependencies() -> list:
    dependencies = []
    if settings.enable_limiter:
        dependencies.append(
            Depends(
                RateLimiter(
                    times=settings.rate_limit_requests_per_interval,
                    seconds=settings.requests_interval,
                )
            )
        )
    return dependencies
