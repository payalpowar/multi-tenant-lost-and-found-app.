from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from database.database import Base


class Item(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.tenant_id"),
        nullable=False,
        index=True
    )

    name = Column(String(100), nullable=False)

    description = Column(String(255), nullable=False)

    color = Column(String(100), nullable=False)

    brand = Column(String(100), nullable=False)

    material = Column(String(100), nullable=False)

    tags = Column(String(255), nullable=False)

    category = Column(String(100), nullable=False)

    image_url = Column(String(255), nullable=False)

    location = Column(String(255), nullable=False)

    status = Column(String(20), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
