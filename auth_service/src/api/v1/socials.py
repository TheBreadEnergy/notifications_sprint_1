import os
from http import HTTPStatus

from async_oauthlib import OAuth2Session
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.core.config import settings
from src.core.extensions import get_providers
from src.models.user import SocialNetworksEnum
from src.schemas.result import GenericResult
from src.schemas.token import Token
from src.services.auth import AuthServiceABC
from src.services.social_providers import SocialNetworkProvider, get_provider
from src.services.user import UserServiceABC

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(settings.base_dir, "templates"))


@router.get("/", response_class=HTMLResponse)
def main_page(
    request: Request,
    code: str | None = Query(None, description="Code from auth provider"),
    providers: dict[SocialNetworksEnum, OAuth2Session] = Depends(get_providers),
):
    google_authorization_url, state = providers[
        SocialNetworksEnum.Google
    ].authorization_url(settings.google_auth_base_url)
    yandex_authorization_url, state = providers[
        SocialNetworksEnum.Yandex
    ].authorization_url(settings.yandex_auth_base_url)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "google_authorization_url": google_authorization_url,
            "yandex_authorization_url": yandex_authorization_url,
            "code": code,
        },
    )


@router.post(
    "/login/{provider_name}",
    response_model=Token,
)
async def login_by_social_network(
    code: str = Query(None, description="Code from auth provider"),
    provider: SocialNetworkProvider = Depends(get_provider),
    user_service: UserServiceABC = Depends(),
    auth: AuthServiceABC = Depends(),
):
    user = await provider.process_user(code, user_service)

    token: GenericResult[Token] = await auth.login_by_oauth(
        login=user.response.login,
    )
    if not token.is_success:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="login or/and password incorrect"
        )

    return token.response
