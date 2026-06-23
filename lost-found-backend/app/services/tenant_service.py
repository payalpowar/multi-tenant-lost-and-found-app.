from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.tenant_repository import TenantRepository


class TenantService:

    @staticmethod
    def create_tenant(
        db: Session,
        tenant_data: dict
    ):
        return TenantRepository.create_tenant(db, tenant_data)

    @staticmethod
    def get_tenant(
        db: Session,
        tenant_id: int
    ):
        tenant = TenantRepository.get_tenant_by_id(db, tenant_id)

        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )

        return tenant

    @staticmethod
    def get_all_tenants(db: Session):
        return TenantRepository.get_all_tenants(db)

    @staticmethod
    def update_tenant(
        db: Session,
        tenant_id: int,
        tenant_data: dict
    ):
        tenant = TenantRepository.get_tenant_by_id(db, tenant_id)

        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )

        return TenantRepository.update_tenant(db, tenant, tenant_data)

    @staticmethod
    def delete_tenant(
        db: Session,
        tenant_id: int
    ):
        tenant = TenantRepository.get_tenant_by_id(db, tenant_id)

        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )

        TenantRepository.delete_tenant(db, tenant)

        return {"message": "Tenant deleted successfully"}
