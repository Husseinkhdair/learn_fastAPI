from domain.auth.entities.user_entitiy import UserDBEntity
from domain.auth.repository.auth_repository import AuthRepository

class AuthRepositoryImp(AuthRepository):
    def __init__(self, data_source:AuthRepository):
        self.data_source = data_source

    async def register_user(self, user_entity: UserDBEntity):
        return await self.data_source.register_user(user_entity)

    async def login_user(self, email: str, password: str):
        return await self.data_source.login_user(email, password)
