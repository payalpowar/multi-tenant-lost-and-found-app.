from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from auth.dependencies import CurrentUser, get_current_user
from database.database import get_db
from schemas.claim import ClaimCreate, ClaimUpdate, ClaimResponse, ClaimImageResponse
from services.claim_service import ClaimService

router = APIRouter(
    prefix="/claims",
    tags=["Claims"]
)


@router.post(
    "/",
    response_model=ClaimResponse,
    status_code=201
)
def create_claim(
    payload: ClaimCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    claim_data = payload.model_dump()
    claim_data["user_id"] = current_user["user_id"]
    return ClaimService.create_claim(db, claim_data)


@router.get(
    "/",
    response_model=List[ClaimResponse]
)
def get_all_claims(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ClaimService.get_all_claims(db, current_user["tenant_id"])


@router.get(
    "/item/{item_id}",
    response_model=List[ClaimResponse]
)
def get_claims_by_item(
    item_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ClaimService.get_claims_by_item(
        db,
        item_id,
        current_user["tenant_id"]
    )


@router.get(
    "/user/{user_id}",
    response_model=List[ClaimResponse]
)
def get_claims_by_user(
    user_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ClaimService.get_claims_by_user(
        db,
        user_id,
        current_user["tenant_id"]
    )


@router.post(
    "/{claim_id}/image",
    response_model=ClaimImageResponse
)
async def upload_claim_image(
    claim_id: int,
    image: UploadFile = File(...),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    claim = await ClaimService.upload_image(
        db,
        claim_id,
        current_user["tenant_id"],
        image
    )
    return ClaimImageResponse(
        claim_id=claim.claim_id,
        image_url=claim.image_url
    )


@router.get(
    "/{claim_id}",
    response_model=ClaimResponse
)
def get_claim(
    claim_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ClaimService.get_claim(db, claim_id, current_user["tenant_id"])


@router.put(
    "/{claim_id}",
    response_model=ClaimResponse
)
def update_claim(
    claim_id: int,
    payload: ClaimUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ClaimService.update_claim(
        db,
        claim_id,
        current_user["tenant_id"],
        payload.model_dump(exclude_unset=True)
    )


@router.delete("/{claim_id}")
def delete_claim(
    claim_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ClaimService.delete_claim(db, claim_id, current_user["tenant_id"])
