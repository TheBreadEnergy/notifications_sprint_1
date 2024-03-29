from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.models import gather_documents

mongo_client: AsyncIOMotorClient | None = None


async def get_mongo_client() -> AsyncIOMotorClient:
    return mongo_client


async def init(*, client: AsyncIOMotorClient) -> None:
    await init_beanie(
        database=getattr(client, settings.bookmarks_database),
        document_models=gather_documents(),  # type: ignore[arg-type]
    )
