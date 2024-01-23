import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, Integer, String
from sqlalchemy_serializer import SerializerMixin
from src.db.database import Base


@dataclass
class File(Base, SerializerMixin):
    __tablename__ = "files"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String(255), nullable=False, unique=True)
    filename = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    file_type = Column(String(100), nullable=True)
    short_name = Column(String(24), nullable=False, unique=True)
    created = Column(DateTime, default=datetime.utcnow)
