from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ClaimCreate(BaseModel):
    item_id: int
    proof: str
    remarks: str
    status: str


class ClaimUpdate(BaseModel):
    proof: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[str] = None


class ClaimResponse(BaseModel):
    claim_id: int
    item_id: int
    user_id: int
    proof: str
    remarks: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
