import logging
import os
from datetime import datetime, timedelta, timezone
from enum import Enum
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status

from core.errors.AuthException import ErrorServerException

logger = logging.getLogger(__name__)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "my-super-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", "5"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class TokenPayload:
    def __init__(
        self,
        user_id: str,
        role: Role,
        expires_delta: timedelta | None = None
    ):
        self.user_id = user_id
        self.role = role
        self.expires_delta = expires_delta

    @classmethod
    def from_dict(cls, data: dict) -> "TokenPayload":
        return cls(
            user_id=str(data.get("user_id") or data.get("id")),
            role=Role(data.get("role")),
            expires_delta=data.get("expires_delta")
        )

    def to_dict(self, default_days: int = ACCESS_TOKEN_EXPIRE_DAYS, token_type: str = "access") -> dict:
        delta = self.expires_delta if self.expires_delta else timedelta(days=default_days)
        expire_at = datetime.now(timezone.utc) + delta

        return {
            "user_id": str(self.user_id),
            "role": self.role.value,
            "type": token_type,
            "exp": expire_at
        }


def create_access_token(payload: TokenPayload) -> str:
    """Creates a JWT Access Token."""
    try:
        token_data = payload.to_dict(default_days=ACCESS_TOKEN_EXPIRE_DAYS, token_type="access")
        return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.exception("Failed to create access token: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": ErrorServerException().message}
        )


def create_refresh_token(payload: TokenPayload) -> str:
    """Creates a JWT Refresh Token."""
    try:
        token_data = payload.to_dict(default_days=REFRESH_TOKEN_EXPIRE_DAYS, token_type="refresh")
        return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.exception("Failed to create refresh token: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": ErrorServerException().message}
        )


def decode_token(token: str) -> TokenPayload:
    """Decodes and validates a JWT token."""
    try:
        payload_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload.from_dict(payload_data)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Token has expired"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Could not validate credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )