from domain.auth.entities.user_entitiy import UserDBEntity, UserEntity
from domain.auth.repository.auth_repository import AuthRepository
from core import Result


class RegisterUserUseCase:
    def __init__(self, user_repository: AuthRepository):
        self.user_repository = user_repository

    async def execute(self, user_entity: UserDBEntity) -> Result[UserEntity]:
        return await self.user_repository.register_user(user_entity)
