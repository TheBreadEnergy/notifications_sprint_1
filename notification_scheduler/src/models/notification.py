from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from src.core.config import settings
from src.models.base import Base


class RecurringNotification(Base):
    __tablename__ = "recurring_notifications"
    __table_args__ = {"schema": settings.db_schema}

    id = Column(UUID(as_uuid=True), primary_key=True)
    template_id = Column(UUID(as_uuid=True))
    user_ids = Column(ARRAY(UUID(as_uuid=True)))
    notification_channel_type = Column(Integer)
    subject = Column(String)
    text = Column(Text)
    status = Column(Integer)
    cron_string = Column(Text)
    created = Column(DateTime(timezone=True))
    modified = Column(DateTime(timezone=True))
    last_notified = Column(DateTime(timezone=True), nullable=True)
