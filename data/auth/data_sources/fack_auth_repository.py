from fastapi import HTTPException,status

from core.errors.AuthException import ErrorServerException, PasswordVerificationFailedException
from core.errors.AuthException import InvalidCredentialsException, UserAlreadyExistsException
from core.functions.security import verify_password

from domain.auth.entities.user_entitiy import UserDBEntity, UserEntity
from domain.auth.repository.auth_repository import AuthRepository


class FackAuthRepository(AuthRepository):
    def __init__(self):
        self.users = {}

    async def register_user(self, user_entity: UserDBEntity)-> UserEntity:
        try:
            if user_entity.email in self.users:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": UserAlreadyExistsException().message}

                )
                
            
            user_entity.id = str(len(self.users) + 1)  # Assign a unique ID
            self.users[user_entity.email] = user_entity
            user = UserEntity(
                id=user_entity.id,
                name=user_entity.name,
                age=user_entity.age,
                is_admin=user_entity.is_admin,
                )
            
            return user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error":ErrorServerException().message}
            )

    async def login_user(self, email: str, password: str)-> UserEntity:
        try:
            
            user = self.users.get(email)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error":InvalidCredentialsException().message
                    }
                )
                
            
            try:
                if user and verify_password(password, user.password):
                    user_entity = UserEntity(
                        id=user.id,
                        name=user.name,
                        age=user.age,
                        is_admin=user.is_admin,
                )
                    return user_entity
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "error":InvalidCredentialsException().message
                        }
                    )
            except Exception as e:
                raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail={"error":ErrorServerException().message}
                    )
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={"error":ErrorServerException().message}
                )


