from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ItemCreate(BaseModel):
    name: str
    description: str
    color: str
    brand: str
    material: str
    tags: str
    category: str
    image_url: str
    location: str
    status: str


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    brand: Optional[str] = None
    material: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None


class ItemResponse(BaseModel):
    item_id: int
    tenant_id: int
    name: str
    description: str
    color: str
    brand: str
    material: str
    tags: str
    category: str
    image_url: str
    location: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
