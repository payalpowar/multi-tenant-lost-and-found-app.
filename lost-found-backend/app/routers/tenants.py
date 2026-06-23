from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from schemas.tenant import TenantCreate, TenantUpdate, TenantResponse
from services.tenant_service import TenantService

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


@router.post(
    "/",
    response_model=TenantResponse,
    status_code=201
)
def create_tenant(
    payload: TenantCreate,
    db: Session = Depends(get_db)
):
    return TenantService.create_tenant(db, payload.model_dump())


@router.get(
    "/",
    response_model=List[TenantResponse]
)
def get_all_tenants(db: Session = Depends(get_db)):
    return TenantService.get_all_tenants(db)


@router.get(
    "/{tenant_id}",
    response_model=TenantResponse
)
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    return TenantService.get_tenant(db, tenant_id)


@router.put(
    "/{tenant_id}",
    response_model=TenantResponse
)
def update_tenant(
    tenant_id: int,
    payload: TenantUpdate,
    db: Session = Depends(get_db)
):
    return TenantService.update_tenant(
        db,
        tenant_id,
        payload.model_dump(exclude_unset=True)
    )


@router.delete("/{tenant_id}")
def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    return TenantService.delete_tenant(db, tenant_id)
