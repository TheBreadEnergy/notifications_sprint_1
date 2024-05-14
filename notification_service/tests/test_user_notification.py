from unittest.mock import AsyncMock

import pytest
from src.models.base import NotificationStatus
from src.services.user_notification import UserNotificationService


@pytest.mark.asyncio
async def test_default_user_notifications():
    mock_repository = AsyncMock()
    service = UserNotificationService(repository=mock_repository)
    await service.get_all_notifications(status=None, skip=0, limit=100)
    mock_repository.gets.assert_called_once_with(status=None, skip=0, limit=100)


@pytest.mark.asyncio
async def test_pending_user_notifications():
    mock_repository = AsyncMock()
    service = UserNotificationService(repository=mock_repository)
    await service.get_all_notifications(
        status=NotificationStatus.pending, skip=0, limit=100
    )
    mock_repository.gets.assert_called_once_with(
        status=NotificationStatus.pending, skip=0, limit=100
    )
