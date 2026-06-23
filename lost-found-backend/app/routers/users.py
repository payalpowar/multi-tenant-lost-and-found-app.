from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from schemas.user import UserCreate, UserUpdate, UserResponse
from services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    return UserService.create_user(db, payload.model_dump())


@router.get(
    "/",
    response_model=List[UserResponse]
)
def get_all_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return UserService.get_user(db, user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db)
):
    return UserService.update_user(
        db,
        user_id,
        payload.model_dump(exclude_unset=True)
    )


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return UserService.delete_user(db, user_id)
