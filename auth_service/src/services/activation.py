from abc import ABC, abstractmethod
from uuid import UUID

from src.exceptions.user_not_found import UserNotFoundException
from src.models.user import User
from src.services.base import UnitOfWork
from src.services.event_handler import EventHandlerABC
from src.services.user import UserRepositoryABC


class ActivationServiceABC(ABC):
    @abstractmethod
    async def activate_user_account(self, user_id: UUID) -> User:
        ...


class ActivationService(ActivationServiceABC):
    def __init__(
        self,
        repository: UserRepositoryABC,
        uow: UnitOfWork,
        event_handler: EventHandlerABC,
    ):
        self._repository = repository
        self._uow = uow
        self._event_handler = event_handler

    async def activate_user_account(self, user_id: UUID) -> User:
        user = await self._repository.get(entity_id=user_id)
        if not user:
            raise UserNotFoundException()
        user.activate_account()
        await self._uow.commit()
        await self._event_handler.handle_activation(user_id=user_id)
        return user
