from core.Result import Result
from core.functions.jwt import decode_token, create_access_token, create_refresh_token

class RefreshTokenUseCase:
    def __init__(self):
        pass

    async def execute(self, refresh_token: str) -> Result[dict]:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                return Result.failure("Invalid token type. Refresh token required.")

            user_id = payload.get("id")
            role = payload.get("role", "user")

            if not user_id:
                return Result.failure("Invalid token payload")

            new_access_token = create_access_token(user_id=user_id, role=role)
            new_refresh_token = create_refresh_token(user_id=user_id, role=role)

            return Result.success({
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            })
        except Exception as e:
            return Result.failure(str(e))
