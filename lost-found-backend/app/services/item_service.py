from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from repositories.item_repository import ItemRepository
from repositories.tenant_repository import TenantRepository
from storage.s3_service import upload_image as upload_image_to_storage

VALID_STATUSES = ["lost", "found", "claimed"]


class ItemService:

    @staticmethod
    def create_item(
        db: Session,
        item_data: dict
    ):
        if not TenantRepository.get_tenant_by_id(db, item_data["tenant_id"]):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )

        if item_data["status"] not in VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status. Must be one of: lost, found, claimed"
            )

        item_data.setdefault("image_url", "")

        return ItemRepository.create_item(db, item_data)

    @staticmethod
    def get_item(
        db: Session,
        item_id: int,
        tenant_id: int
    ):
        item = ItemRepository.get_item_by_id(db, item_id, tenant_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        return item

    @staticmethod
    def get_all_items(
        db: Session,
        tenant_id: int
    ):
        if not TenantRepository.get_tenant_by_id(db, tenant_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )

        return ItemRepository.get_all_items(db, tenant_id)

    @staticmethod
    def update_item(
        db: Session,
        item_id: int,
        tenant_id: int,
        item_data: dict
    ):
        item = ItemRepository.get_item_by_id(db, item_id, tenant_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        if item_data.get("status") and item_data["status"] not in VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status. Must be one of: lost, found, claimed"
            )

        return ItemRepository.update_item(db, item, item_data)

    @staticmethod
    def delete_item(
        db: Session,
        item_id: int,
        tenant_id: int
    ):
        item = ItemRepository.get_item_by_id(db, item_id, tenant_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        ItemRepository.delete_item(db, item)

        return {"message": "Item deleted successfully"}

    @staticmethod
    async def upload_image(
        db: Session,
        item_id: int,
        tenant_id: int,
        image: UploadFile
    ):
        item = ItemRepository.get_item_by_id(db, item_id, tenant_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        image_url = await upload_image_to_storage(
            image,
            f"tenant_{tenant_id}/items/{item_id}"
        )

        return ItemRepository.update_item(
            db,
            item,
            {"image_url": image_url}
        )
