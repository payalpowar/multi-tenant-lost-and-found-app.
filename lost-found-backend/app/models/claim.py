from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from database.database import Base


class Claim(Base):
    __tablename__ = "claims"

    claim_id = Column(Integer, primary_key=True, index=True)

    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    proof = Column(String(255), nullable=False)

    remarks = Column(String(255), nullable=False)

    status = Column(String(20), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    image_url = Column(String(255), nullable=True)