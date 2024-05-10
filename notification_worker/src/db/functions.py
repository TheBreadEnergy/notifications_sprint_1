import logging

from sqlalchemy import select
from src.db.postgres import async_session
from src.models.template import Template
from src.models.user import User


async def get_user_by_id(user_id: str) -> User:
    async with async_session() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            logging.error("Пользователь не найден")
        return user


async def get_template_by_id(template_id: str) -> Template:
    async with async_session() as session:
        # fixme в админ сервисе число, вместо uuid указано
        query = select(Template).where(Template.id == int(template_id))
        result = await session.execute(query)
        template = result.scalars().first()
        if not template:
            logging.error("Шаблон не найден")
        return template
