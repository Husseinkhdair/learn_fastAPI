from fastapi import HTTPException, status

from core.errors.AuthException import AccessTokenCreationFailedException, ErrorServerException, RefreshTokenCreationFailedException
from core.functions.jwt import TokenPayload, create_access_token, create_refresh_token, decode_token


class RefreshTokenUseCase:
    def __init__(self):
        pass

    async def execute(self, refresh_token: str) -> dict:
        try:
            payload: TokenPayload = decode_token(refresh_token)

            try:
                new_access_token = create_access_token(payload)
            except Exception as e:
                raise AccessTokenCreationFailedException() from e

            # 3. إنشاء Refresh Token
            try:
                new_refresh_token = create_refresh_token(payload)
            except Exception as e:
                raise RefreshTokenCreationFailedException() from e

            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": ErrorServerException().message}
            )

       
