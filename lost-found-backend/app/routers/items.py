from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from auth.dependencies import CurrentUser, get_current_user
from database.database import get_db
from schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemImageResponse
from services.item_service import ItemService

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=201
)
def create_item(
    payload: ItemCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item_data = payload.model_dump()
    item_data["tenant_id"] = current_user["tenant_id"]
    return ItemService.create_item(db, item_data)


@router.get(
    "/",
    response_model=List[ItemResponse]
)
def get_all_items(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ItemService.get_all_items(db, current_user["tenant_id"])


@router.post(
    "/{item_id}/image",
    response_model=ItemImageResponse
)
async def upload_item_image(
    item_id: int,
    image: UploadFile = File(...),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = await ItemService.upload_image(
        db,
        item_id,
        current_user["tenant_id"],
        image
    )
    return ItemImageResponse(
        item_id=item.item_id,
        image_url=item.image_url
    )


@router.get(
    "/{item_id}",
    response_model=ItemResponse
)
def get_item(
    item_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ItemService.get_item(db, item_id, current_user["tenant_id"])


@router.put(
    "/{item_id}",
    response_model=ItemResponse
)
def update_item(
    item_id: int,
    payload: ItemUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ItemService.update_item(
        db,
        item_id,
        current_user["tenant_id"],
        payload.model_dump(exclude_unset=True)
    )


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ItemService.delete_item(db, item_id, current_user["tenant_id"])
