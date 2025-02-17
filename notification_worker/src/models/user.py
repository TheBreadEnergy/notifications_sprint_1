from sqlalchemy import UUID, Column, String
from src.core.config import settings
from src.models.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": settings.db_schema}

    id: str = Column(UUID, primary_key=True)
    login: str = Column(String)
    email: str = Column(String)
    first_name: str = Column(String)
    last_name: str = Column(String)
