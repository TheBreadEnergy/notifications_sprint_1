from uuid import uuid4

from sqlalchemy import UUID, Column, String, Text
from sqlalchemy.orm import relationship
from src.db.postgres import Base
from src.models.user_role import UserRole


class Role(Base):
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text)
    users = relationship(
        "User", secondary=UserRole.__tablename__, back_populates="roles"
    )

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Role {self.name}>"

    def update_role(self, name: str, description: str | None):
        self.name = name
        self.description = description
