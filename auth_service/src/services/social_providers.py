from abc import ABC

import httpx
from async_oauthlib import OAuth2Session
from fastapi import HTTPException, status
from src.core.config import settings
from src.models.user import SocialNetworksEnum, User
from src.schemas.result import GenericResult
from src.schemas.user import SocialUser
from src.services.user import UserServiceABC


class SocialNetworkProvider(ABC):
    social_name = SocialNetworksEnum
    auth_token_url: str
    userinfo_url: str
    client_secret: str
    client_id: str

    def __init__(self):
        self.session = None

    @classmethod
    async def create(cls):
        instance = cls()
        await instance.init_session()
        return instance

    async def init_session(self):
        self.session = OAuth2Session(
            self.client_id, redirect_uri=settings.social_auth_redirect_url
        )

    async def process_user(
        self, code: str, user_service: UserServiceABC
    ) -> GenericResult[User]:
        data = await self.fetch_data(code)
        user = await user_service.get_or_create_user(
            social=SocialUser(
                social_name=self.social_name, email=data["default_email"], **data
            )
        )
        return user

    async def fetch_data(self, code: str):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.social_auth_redirect_url,
        }
        async with httpx.AsyncClient() as client:
            token_response = await client.post(self.auth_token_url, data=data)
            token_response.raise_for_status()
            token = token_response.json()["access_token"]

            headers = {"Authorization": f"Bearer {token}"}
            userinfo_response = await client.get(self.userinfo_url, headers=headers)
            userinfo_response.raise_for_status()
            return userinfo_response.json()


class Yandex(SocialNetworkProvider):
    social_name = SocialNetworksEnum.Yandex
    auth_token_url = settings.yandex_auth_token_url
    userinfo_url = settings.yandex_userinfo_url
    client_secret = settings.yandex_client_secret
    client_id = settings.yandex_client_id


class Google(SocialNetworkProvider):
    social_name = SocialNetworksEnum.Google
    auth_token_url = settings.google_auth_token_url
    userinfo_url = settings.google_userinfo_url
    client_secret = settings.google_client_secret
    client_id = settings.google_client_id


async def get_provider(provider_name: SocialNetworksEnum) -> SocialNetworkProvider:
    providers = {
        SocialNetworksEnum.Yandex: Yandex,
        SocialNetworksEnum.Google: Google,
    }
    provider_class = providers.get(provider_name)
    if not provider_class:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported social network"
        )

    return await provider_class.create()
