from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from repositories.claim_repository import ClaimRepository
from repositories.item_repository import ItemRepository
from repositories.user_repository import UserRepository
from repositories.tenant_repository import TenantRepository
from storage.s3_service import upload_image as upload_image_to_storage

VALID_STATUSES = ["pending", "approved", "rejected"]


class ClaimService:

    @staticmethod
    def create_claim(
        db: Session,
        claim_data: dict
    ):
        user = UserRepository.get_user_by_id(
            db,
            claim_data["user_id"]
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        item = ItemRepository.get_item_by_id(
            db,
            claim_data["item_id"],
            user.tenant_id
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        if claim_data["status"] not in VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status. Must be one of: pending, approved, rejected"
            )

        claim_data.setdefault("image_url", None)

        return ClaimRepository.create_claim(db, claim_data)

    @staticmethod
    def get_claim(
        db: Session,
        claim_id: int,
        tenant_id: int
    ):
        if not TenantRepository.get_tenant_by_id(db, tenant_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )

        claim = ClaimRepository.get_claim_by_id(db, claim_id, tenant_id)

        if not claim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Claim not found"
            )

        return claim

    @staticmethod
    def get_all_claims(
        db: Session,
        tenant_id: int
    ):
        if not TenantRepository.get_tenant_by_id(db, tenant_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )

        return ClaimRepository.get_all_claims(db, tenant_id)

    @staticmethod
    def get_claims_by_item(
        db: Session,
        item_id: int,
        tenant_id: int
    ):
        if not ItemRepository.get_item_by_id(db, item_id, tenant_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        return ClaimRepository.get_claims_by_item(db, item_id, tenant_id)

    @staticmethod
    def get_claims_by_user(
        db: Session,
        user_id: int,
        tenant_id: int
    ):
        user = UserRepository.get_user_by_id(db, user_id)

        if not user or user.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return ClaimRepository.get_claims_by_user(db, user_id, tenant_id)

    @staticmethod
    def update_claim(
        db: Session,
        claim_id: int,
        tenant_id: int,
        claim_data: dict
    ):
        claim = ClaimRepository.get_claim_by_id(db, claim_id, tenant_id)

        if not claim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Claim not found"
            )

        if claim_data.get("status") and claim_data["status"] not in VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status. Must be one of: pending, approved, rejected"
            )

        return ClaimRepository.update_claim(db, claim, claim_data)

    @staticmethod
    def delete_claim(
        db: Session,
        claim_id: int,
        tenant_id: int
    ):
        claim = ClaimRepository.get_claim_by_id(db, claim_id, tenant_id)

        if not claim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Claim not found"
            )

        ClaimRepository.delete_claim(db, claim)

        return {"message": "Claim deleted successfully"}

    @staticmethod
    async def upload_image(
        db: Session,
        claim_id: int,
        tenant_id: int,
        image: UploadFile
    ):
        claim = ClaimRepository.get_claim_by_id(db, claim_id, tenant_id)

        if not claim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Claim not found"
            )

        image_url = await upload_image_to_storage(
            image,
            f"tenant_{tenant_id}/claims/{claim_id}"
        )

        return ClaimRepository.update_image_url(db, claim, image_url)
