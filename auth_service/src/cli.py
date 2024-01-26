import asyncio
import logging
from functools import wraps
from typing import Annotated

import typer
import uvicorn
from pydantic import EmailStr
from src.core.config import Roles
from src.core.logging import LOGGING
from src.db.postgres import async_session
from src.models.role import Role
from src.models.user import User

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
    email: Annotated[EmailStr, typer.Argument()],
):
    async with async_session() as session:
        try:
            super_admin_role = Role(
                name=str(Roles.SUPER_ADMIN), description="Super Admin privilege"
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
