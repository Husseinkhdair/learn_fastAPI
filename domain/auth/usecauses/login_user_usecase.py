from fastapi import HTTPException, status

from core.errors.AuthException import ErrorServerException
from core.functions.jwt import Role, TokenPayload, create_access_token, create_refresh_token
from domain.auth.repository.auth_repository import AuthRepository


class LoginUserUseCase:
    def __init__(self, user_repository: AuthRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, password: str) -> dict:
        try:
            user = await self.user_repository.login_user(email, password)
            role = Role.ADMIN if user.is_admin else Role.USER

            payload = TokenPayload(
                user_id=str(user.id),
                role=role
            )

            access_token = create_access_token(payload)
            refresh_token = create_refresh_token(payload)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": user
            }
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": ErrorServerException().message}
            )

            
            
        

        
        





        