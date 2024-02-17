import datetime
import enum
from typing import List, Self
from uuid import uuid4

from passlib.hash import pbkdf2_sha256
from pydantic import EmailStr
from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, relationship
from src.db.postgres import Base
from src.models.role import Role
from src.models.user_history import UserHistory
from src.models.user_role import UserRole


# TODO: Place this in another file
class SocialNetworksEnum(enum.Enum):
    Yandex = "Yandex"
    Google = "Google"


class SocialAccount(Base):
    __tablename__ = "social_account"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="social_accounts", cascade="all, delete")

    social_id = Column(Text, nullable=False)
    social_name = Column(Enum(SocialNetworksEnum))

    __table_args__ = (UniqueConstraint("social_id", "social_name", name="social_pk"),)

    def __init__(
        self,
        social_id: str,
        social_name: SocialNetworksEnum,
    ) -> None:
        self.social_id = social_id
        self.social_name = social_name

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(255))
    roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary=UserRole.__tablename__,
        back_populates="users",
        cascade="all, delete",
    )
    history: Mapped[List["UserHistory"]] = relationship(
        "UserHistory", back_populates="user", cascade="all, delete-orphan"
    )
    social_accounts: Mapped[List["SocialAccount"]] = relationship(
        "SocialAccount",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    created = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC)
    )
    updated = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC),
        onupdate=datetime.datetime.now(datetime.UTC),
    )

    def __init__(
        self,
        login: str,
        password: str,
        first_name: str,
        last_name: str,
        email: EmailStr,
    ) -> None:
        self.login = login
        self.password_hash = pbkdf2_sha256.hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.social_accounts = []

    def check_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password_hash)

    def change_password(self, old_password: str, new_password: str) -> bool:
        if not self.check_password(old_password):
            return False
        self.password_hash = pbkdf2_sha256.hash(new_password)
        return True

    def __repr__(self) -> str:
        return f"<User {self.login}>"

    def update_personal(
        self,
        login: str | None,
        first_name: str | None,
        last_name: str | None,
        email: EmailStr | None,
    ) -> Self:
        self.login = login or self.login
        self.first_name = first_name or self.first_name
        self.last_name = last_name or self.last_name
        self.email = email or self.email
        return self

    def update_login(self, login: str) -> Self:
        self.login = login if login != "" else self.login
        return Self

    def assign_role(self, role: Role):
        if not self.has_role(role.name):
            self.roles.append(role)

    def remove_role(self, role: Role) -> None:
        if role in self.roles:
            self.roles.remove(role)

    def has_role(self, role_name: str) -> bool:
        for role in self.roles:
            if role.name == role_name:
                return True
        return False

    def add_user_session(self, session: UserHistory) -> None:
        self.history.append(session)

    def add_social_account(self, social_account: SocialAccount) -> None:
        self.social_accounts.append(social_account)
