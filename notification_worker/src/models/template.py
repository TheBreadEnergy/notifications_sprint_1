from sqlalchemy import Column, Integer, String
from src.core.config import settings
from src.models.base import Base


class Template(Base):
    __tablename__ = "templates"
    __table_args__ = {"schema": settings.db_schema}

    # fixme в админ сервисе число, вместо uuid указано
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    layout: str = Column(String)
