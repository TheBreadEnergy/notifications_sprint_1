import asyncio
import logging
from functools import wraps
from typing import Annotated

import typer
import uvicorn
from sqlalchemy import select
from src.core.logging import LOGGING
from src.db.postgres import async_session
from src.models.role import Role
from src.models.user import User
from src.schemas.role import Roles

cli = typer.Typer()


@cli.command()
def start_app():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.INFO,
    )


def typer_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@cli.command()
@typer_async
async def create_superuser(
    login: Annotated[str, typer.Argument()],
    password: Annotated[str, typer.Argument()],
    first_name: Annotated[str, typer.Argument()],
    last_name: Annotated[str, typer.Argument()],
    email: Annotated[str, typer.Argument()],
):
    async with async_session() as session:
        try:
            user_statement = select(User).where(User.login == login)
            role_statement = select(Role).where(Role.name == Roles.SUPER_ADMIN)
            user_result = await session.execute(user_statement)
            role_result = await session.execute(role_statement)
            if user_result.scalar_one_or_none():
                return
            if role_result.scalar_one_or_none():
                return

            super_admin_role = Role(
                name=Roles.SUPER_ADMIN, description="Super Admin privilege"
            )
            super_admin_user = User(
                login=login,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            session.add(super_admin_role)
            session.add(super_admin_user)
            super_admin_user.assign_role(super_admin_role)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
