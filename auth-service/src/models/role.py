from uuid import uuid4

from sqlalchemy import Column, String, Text, UUID

from src.db.postgres import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text)

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Role {self.name}>"

    def update_role(self, name: str, description: str | None):
        self.name = name
        self.description = description
