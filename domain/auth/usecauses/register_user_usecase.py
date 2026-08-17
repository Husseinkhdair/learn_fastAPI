from core.Result import Result
from core.functions.security import hash_password
from core.functions.jwt import create_access_token, create_refresh_token
from domain.auth.entities.user_entitiy import UserDBEntity
from domain.auth.repository.auth_repository import AuthRepository


class RegisterUserUseCase:
    def __init__(self, user_repository: AuthRepository):
        self.user_repository = user_repository

    async def execute(self, user_entity: UserDBEntity) -> Result[dict]:
        user_entity.password = hash_password(user_entity.password)
        res = await self.user_repository.register_user(user_entity)

        if not res.is_success:
            return Result.failure(res.error)

        created_user = res.value
        role = "admin" if created_user.is_admin else "user"

        access_token = create_access_token(user_id=created_user.id, role=role)
        refresh_token = create_refresh_token(user_id=created_user.id, role=role)

        return Result.success({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": created_user
        })
