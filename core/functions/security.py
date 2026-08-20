import bcrypt
from fastapi import HTTPException,status

from core.errors.AuthException import ErrorServerException


def hash_password(password: str) -> str:
    try:
        # تحويل النص إلى Bytes مع اقتطاع أول 72 بايت لتجنب قيود bcrypt
        password_bytes = password.encode("utf-8")[:72]
        # توليد Salt وتشفير كلمة المرور
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error":ErrorServerException().message}
            )
    
    


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        password_bytes = plain_password.encode("utf-8")[:72]
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error":ErrorServerException().message}
            )