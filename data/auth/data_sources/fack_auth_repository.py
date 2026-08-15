from domain.auth.entities.user_entitiy import UserDBEntity
from domain.auth.repository.auth_repository import AuthRepository


class FackAuthRepository(AuthRepository):
    def __init__(self):
        self.users = {}

    async def register_user(self, user_entity: UserDBEntity):
        try:
            

    async def login_user(self, email: str, password: str):
        raise NotImplementedError


