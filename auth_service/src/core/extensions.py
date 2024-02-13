from async_oauthlib import OAuth2Session
from src.core.config import settings
from src.models.user import SocialNetworksEnum

google = OAuth2Session(
    settings.google_client_id, redirect_uri=settings.social_auth_redirect_url
)
yandex = OAuth2Session(
    settings.yandex_client_id, redirect_uri=settings.social_auth_redirect_url
)


async def get_providers() -> dict[SocialNetworksEnum, OAuth2Session]:
    return {
        SocialNetworksEnum.Google: google,
        SocialNetworksEnum.Yandex: yandex,
    }
