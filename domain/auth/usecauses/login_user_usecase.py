from core.Result import Result
from core.functions.jwt import create_access_token, create_refresh_token
from domain.auth.repository.auth_repository import AuthRepository


class LoginUserUseCase:
    def __init__(self, user_repository: AuthRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, password: str) -> Result[dict]:
        res = await self.user_repository.login_user(email, password)

        if not res.is_success:
            return Result.failure(res.error)

        user = res.value
        role = "admin" if user.is_admin else "user"

        access_token = create_access_token(user_id=user.id, role=role)
        refresh_token = create_refresh_token(user_id=user.id, role=role)

        return Result.success({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        })