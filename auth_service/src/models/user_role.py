from sqlalchemy import UUID, Column, ForeignKey, UniqueConstraint
from src.db.postgres import Base


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="unique_user_role"),)
