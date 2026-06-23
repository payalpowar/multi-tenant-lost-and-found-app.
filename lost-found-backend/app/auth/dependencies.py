from typing import Any, TypedDict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from auth.jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class CurrentUser(TypedDict):
    user_id: int
    tenant_id: int
    role: str
    email: str


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, Any] = verify_access_token(token)
    except JWTError:
        raise credentials_exception

    required_claims = ("user_id", "tenant_id", "role", "email")
    if not all(claim in payload for claim in required_claims):
        raise credentials_exception

    return CurrentUser(
        user_id=int(payload["user_id"]),
        tenant_id=int(payload["tenant_id"]),
        role=str(payload["role"]),
        email=str(payload["email"]),
    )
