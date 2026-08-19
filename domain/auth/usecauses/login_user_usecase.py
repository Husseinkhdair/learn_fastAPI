from core.functions.jwt import create_access_token, create_refresh_token
from domain.auth.repository.auth_repository import AuthRepository


class LoginUserUseCase:
    def __init__(self, user_repository: AuthRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, password: str) -> dict:
        try:
            res = await self.user_repository.login_user(email, password)
            user = res.value
            role = "admin" if user.is_admin else "user"

            access_token = create_access_token(user_id=user.id, role=role)
            refresh_token = create_refresh_token(user_id=user.id, role=role)

            return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
            }
        except Exception as e:
                raise
            
            
        

        
        





        