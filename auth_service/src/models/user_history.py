from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from src.db.postgres import Base


class UserHistory(Base):
    __tablename__ = "user_history"
    __table_args__ = (
        UniqueConstraint("id", "user_device_type"),
        {
            "postgresql_partition_by": "LIST (user_device_type)",
        },
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="history")
    attempted = Column(DateTime(timezone=True), default=datetime.now(UTC))
    user_agent = Column(String(255))
    user_device_type = Column(Text, primary_key=True)
    success = Column(Boolean, default=True, nullable=False)

    def __init__(self, user_id, attempted, user_agent, user_device_type, success):
        self.user_id = user_id
        self.attempted = attempted
        self.user_agent = user_agent
        self.success = success
        self.user_device_type = user_device_type

    def __repr__(self):
        return f"<UserHistory {self.id}>"
