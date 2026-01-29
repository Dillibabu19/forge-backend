import uuid
from datetime import datetime
from sqlalchemy import Boolean, String, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from typing import Optional
from app.db.session import Base

class RefreshTokens(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[uuid.UUID] = mapped_column(Uuid(),primary_key=True,index=True,default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(),ForeignKey("users.id"),nullable=False)

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

    ip_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(),ForeignKey("refresh_tokens.id"))

    replaced_by: Mapped["RefreshTokens"] = relationship(
        back_populates="children",
        remote_side=[id],
        uselist=False
    )

    children: Mapped["RefreshTokens"] = relationship(
        back_populates="replaced_by"
    )
