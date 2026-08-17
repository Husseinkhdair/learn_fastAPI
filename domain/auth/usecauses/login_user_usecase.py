from core.Result import Result
from domain.auth.entities.user_entitiy import UserEntity
from domain.auth.repository.auth_repository import AuthRepository


class LoginUserUseCase:
    def __init__(self, user_repository: AuthRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, password: str) -> Result[UserEntity]:
        return await self.user_repository.login_user(email, password)