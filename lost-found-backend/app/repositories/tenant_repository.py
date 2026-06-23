from sqlalchemy.orm import Session

from models.tenant import Tenant


class TenantRepository:

    @staticmethod
    def create_tenant(
        db: Session,
        tenant_data: dict
    ):
        tenant = Tenant(**tenant_data)

        db.add(tenant)
        db.commit()
        db.refresh(tenant)

        return tenant

    @staticmethod
    def get_tenant_by_id(
        db: Session,
        tenant_id: int
    ):
        return db.query(Tenant).filter(
            Tenant.tenant_id == tenant_id
        ).first()

    @staticmethod
    def get_all_tenants(db: Session):
        return db.query(Tenant).all()

    @staticmethod
    def update_tenant(
        db: Session,
        tenant: Tenant,
        tenant_data: dict
    ):
        for key, value in tenant_data.items():
            if value is not None:
                setattr(tenant, key, value)

        db.commit()
        db.refresh(tenant)

        return tenant

    @staticmethod
    def delete_tenant(
        db: Session,
        tenant: Tenant
    ):
        db.delete(tenant)
        db.commit()
