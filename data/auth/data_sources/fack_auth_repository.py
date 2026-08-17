from core import Result

from domain.auth.entities.user_entitiy import UserDBEntity
from domain.auth.repository.auth_repository import AuthRepository


class FackAuthRepository(AuthRepository):
    def __init__(self):
        self.users = {}

    async def register_user(self, user_entity: UserDBEntity)-> Result[UserDBEntity]:
        try:
            self.users[user_entity.email] = user_entity
            return Result.success(user_entity)
        except Exception as e:
            return Result.failure(str(e))

    async def login_user(self, email: str, password: str)-> Result[UserDBEntity]:
        try:
            user = self.users.get(email)
            if user is None:
                return Result.failure("User not found")
            if user and user.password == password:
                return Result.success(user)
            else:
                return Result.failure("Invalid email or password")
        except Exception as e:
            return Result.failure(str(e))


