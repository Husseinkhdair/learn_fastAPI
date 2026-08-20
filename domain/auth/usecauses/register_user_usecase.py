from fastapi import HTTPException,status

import logging
from core.errors.AuthException import AccessTokenCreationFailedException, ErrorServerException, RefreshTokenCreationFailedException
from core.functions.jwt import Role, TokenPayload, create_access_token, create_refresh_token
from core.functions.security import hash_password
from domain.auth.entities.user_entitiy import UserDBEntity
from domain.auth.repository.auth_repository import AuthRepository

logger = logging.getLogger(__name__)


class RegisterUserUseCase:
    def __init__(self, user_repository: AuthRepository):
        self.user_repository = user_repository

    async def execute(self, user_entity: UserDBEntity) -> dict:
        try:
            user_entity.password = hash_password(user_entity.password)
            created_user = await self.user_repository.register_user(user_entity)
            role = Role.ADMIN if created_user.is_admin else Role.USER

            payload = TokenPayload(user_id=str(created_user.id), role=role)

            try:
                access_token = create_access_token(payload)
            except Exception as e:
                logger.exception("Failed to create access token for user %s: %s", created_user.id, e)
                raise AccessTokenCreationFailedException() from e

            # 3. إنشاء Refresh Token
            try:
                refresh_token = create_refresh_token(payload)
            except Exception as e:
                logger.exception("Failed to create refresh token for user %s: %s", created_user.id, e)
                raise RefreshTokenCreationFailedException() from e

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": created_user
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Unexpected error in RegisterUserUseCase: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": ErrorServerException().message}
            )
