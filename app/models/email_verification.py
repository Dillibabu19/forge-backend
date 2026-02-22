import uuid
from datetime import datetime
from sqlalchemy import String,DateTime,Uuid,ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.db.session import Base

class EmailVerification(Base):
    __tablename__ = "email_verification_tokens"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(),primary_key=True,default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(),ForeignKey("users.id"),nullable=False,index=True)

    token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    is_used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    user = relationship("User", back_populates="email_verifications")

    # server_default=func.now(),