from core.errors.AuthException import AccessTokenCreationFailedException, PasswordHashingFailedException, RefreshTokenCreationFailedException
from core.functions.security import hash_password
from core.functions.jwt import create_access_token, create_refresh_token
from domain.auth.entities.user_entitiy import UserDBEntity
from domain.auth.repository.auth_repository import AuthRepository


class RegisterUserUseCase:
    def __init__(self, user_repository: AuthRepository):
        self.user_repository = user_repository

    async def execute(self, user_entity: UserDBEntity) -> dict:
        try:
            user_entity.password = hash_password(user_entity.password)
        except Exception as e:
            raise PasswordHashingFailedException() from e

        try:
            res = await self.user_repository.register_user(user_entity)
        except Exception as e:
            raise e


        created_user = res
        role = "admin" if created_user.is_admin else "user"

        try:
            access_token = create_access_token(user_id=created_user.id, role=role)

        except Exception as e:
            raise AccessTokenCreationFailedException() from e

        # 3. إنشاء Refresh Token
        try:
            refresh_token = create_refresh_token(user_id=created_user.id, role=role)

        except Exception as e:
            raise RefreshTokenCreationFailedException() from e

        

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": created_user
        }
        
        
