from core.Result import Result
from core.functions.security import hash_password
from domain.auth.entities.user_entitiy import UserDBEntity, UserEntity
from domain.auth.repository.auth_repository import AuthRepository


class RegisterUserUseCase:
    def __init__(self, user_repository: AuthRepository):
        self.user_repository = user_repository

    async def execute(self, user_entity: UserDBEntity) -> Result[UserEntity]:
        user_entity.password = hash_password(user_entity.password)
        return await self.user_repository.register_user(user_entity)

