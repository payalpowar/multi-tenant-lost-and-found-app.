from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from auth.jwt_handler import create_access_token
from auth.password_handler import verify_password
from repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ) -> dict:
        user = UserRepository.get_user_for_login(db, email)

        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={
                "user_id": user.user_id,
                "tenant_id": user.tenant_id,
                "role": user.role,
                "email": user.email,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
