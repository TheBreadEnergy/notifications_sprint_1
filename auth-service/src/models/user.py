import datetime
from typing import List, Self
from uuid import uuid4

from passlib.hash import pbkdf2_sha256
from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.orm import Mapped, relationship
from src.db.postgres import Base
from src.models.role import Role
from src.models.user_history import UserHistory


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(255))
    roles: Mapped[List["Role"]] = relationship(
        "Role", secondary="user_roles", lazy="selectin"
    )
    history: Mapped[List[UserHistory]] = relationship(
        "UserHistory", back_populates="user"
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
        self, login: str, password: str, first_name: str, last_name: str, email: str
    ) -> None:
        self.login = login
        self.password_hash = pbkdf2_sha256.hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

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
        email: str | None,
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
        self.roles.append(role)

    def remove_role(self, role: Role) -> None:
        if role in self.roles:
            self.roles.remove(role)

    def has_role(self, role_name: str) -> bool:
        for role in self.roles:
            if role.name == role_name:
                return True
        return False
