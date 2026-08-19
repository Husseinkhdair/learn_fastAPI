from core.errors.AuthException import AccessTokenCreationFailedException, InvalidTokenException, RefreshTokenCreationFailedException
from core.functions.jwt import decode_token, create_access_token, create_refresh_token

class RefreshTokenUseCase:
    def __init__(self):
        pass

    async def execute(self, refresh_token: str) -> dict:
        try:
            try:
                payload = decode_token(refresh_token)
            except Exception as e:
                raise InvalidTokenException("Invalid or expired refresh token") from e

            user_id = payload.get("id")
            role = payload.get("role", "user")

            if not user_id:
                raise InvalidTokenException()


            try:
                new_access_token = create_access_token(user_id=user_id, role=role)
            except Exception as e:
                raise AccessTokenCreationFailedException() from e

            # 3. إنشاء Refresh Token
            try:
                new_refresh_token = create_refresh_token(user_id=user_id, role=role)
            except Exception as e:
                raise RefreshTokenCreationFailedException() from e

            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }
        except Exception as e:
            raise
       
