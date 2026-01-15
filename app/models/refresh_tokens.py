from datetime import datetime
from sqlalchemy import Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from typing import Optional
from app.db.session import Base

class RefreshTokens(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(primary_key=True,index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)

    token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
    )

    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="refresh_tokens"
    )


