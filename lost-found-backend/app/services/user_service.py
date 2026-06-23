from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from auth.password_handler import hash_password
from repositories.tenant_repository import TenantRepository
from repositories.user_repository import UserRepository

VALID_ROLES = ["admin", "tenant_admin", "user"]


class UserService:

    @staticmethod
    def create_user(
        db: Session,
        user_data: dict
    ):
        if not TenantRepository.get_tenant_by_id(db, user_data["tenant_id"]):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )

        if UserRepository.get_user_by_email(db, user_data["email"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        if UserRepository.get_user_by_username(db, user_data["username"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        if user_data["role"] not in VALID_ROLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role is not valid"
            )

        if len(user_data["password"]) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters"
            )

        user_data["password"] = hash_password(user_data["password"])

        return UserRepository.create_user(db, user_data)

    @staticmethod
    def get_user(
        db: Session,
        user_id: int
    ):
        user = UserRepository.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    @staticmethod
    def get_all_users(db: Session):
        return UserRepository.get_all_users(db)

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        user_data: dict
    ):
        user = UserRepository.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if user_data.get("role") and user_data["role"] not in VALID_ROLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role is not valid"
            )

        return UserRepository.update_user(db, user, user_data)

    @staticmethod
    def delete_user(
        db: Session,
        user_id: int
    ):
        user = UserRepository.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        UserRepository.delete_user(db, user)

        return {"message": "User deleted successfully"}
