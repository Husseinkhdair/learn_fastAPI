from core.errors.AuthException import PasswordVerificationFailedException
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
                raise UserAlreadyExistsException()
            
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
            raise e

    async def login_user(self, email: str, password: str)-> UserEntity:
        try:
            
            user = self.users.get(email)
            if user is None:
                raise InvalidCredentialsException()
            
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
                    raise InvalidCredentialsException()
            except PasswordVerificationFailedException as e:
                raise e
            except InvalidCredentialsException as e:
                raise e
            except Exception as e:
                raise e
        except Exception as e:
            raise e


