import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.db.session import Base

class RolePermissions(Base):
    __tablename__ = "role_permissions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True,index=True,default=uuid.uuid4)

    role_id: Mapped[uuid.UUID] = mapped_column(Uuid(),
        ForeignKey("roles.id",ondelete="CASCADE"),nullable=False
    )

    permission_id: Mapped[uuid.UUID] = mapped_column(Uuid(),
        ForeignKey("permissions.id",ondelete="CASCADE"),nullable=False
    )

    role: Mapped["Roles"] = relationship("Roles",viewonly=True)
    permission: Mapped["Permissions"] = relationship("Permissions", viewonly=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=datetime.now,
    )