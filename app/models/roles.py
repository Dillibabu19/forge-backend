import uuid
import enum
from datetime import datetime
from sqlalchemy import String, DateTime, Uuid, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.db.session import Base

class RoleType(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(),primary_key=True,index=True,default=uuid.uuid4)

    name: Mapped[RoleType] = mapped_column(
        Enum(RoleType,values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=RoleType.USER
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=datetime.now,
    )

    permissions: Mapped[list["Permissions"]] = relationship(
        secondary="role_permissions",
        passive_deletes=True
    )