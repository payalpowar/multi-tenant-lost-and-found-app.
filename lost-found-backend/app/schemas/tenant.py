from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TenantCreate(BaseModel):
    name: str
    address: str


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None


class TenantResponse(BaseModel):
    tenant_id: int
    name: str
    address: str
    created_at: datetime

    class Config:
        from_attributes = True
