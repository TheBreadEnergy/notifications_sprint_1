from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from src.db.postgres import Base


class UserHistory(Base):
    __tablename__ = "user_history"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="history")
    attempted = Column(DateTime(timezone=True), default=datetime.now(UTC))
    user_agent = Column(String(255))
    success = Column(Boolean, default=True, nullable=False)

    def __init__(self, user_id, attempted, user_agent, success):
        self.user_id = user_id
        self.attempted = attempted
        self.user_agent = user_agent
        self.success = success

    def __repr__(self):
        return f"<UserHistory {self.id}>"
