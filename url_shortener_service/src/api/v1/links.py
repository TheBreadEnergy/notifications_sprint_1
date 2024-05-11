from fastapi import APIRouter, Depends, Request
from src.schemas.links import ShortLinkCreateSchema, ShortUrlResponseSchema
from src.services.links import LinksShortenerABC
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/{short_url}", response_class=RedirectResponse)
async def get_full_url(short_url: str, link_service: LinksShortenerABC = Depends()):
    return await link_service.unshorten(url=short_url)


@router.post(
    "/shortify",
    response_model=ShortUrlResponseSchema,
    description="Возвращает скоращенную ссылку",
    response_description="Сокращенная ссылка",
    tags=["Links"],
)
async def shorten_url(
    short_url_request: ShortLinkCreateSchema,
    request: Request,
    link_service: LinksShortenerABC = Depends(),
):
    domain = request.base_url
    short_url = await link_service.shorten(
        url=short_url_request.url, ttl_s=short_url_request.duration
    )
    return ShortUrlResponseSchema(url=f"{domain}{short_url}")
