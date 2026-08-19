from abc import ABC, abstractmethod
from domain.auth.entities.user_entitiy import UserDBEntity, UserEntity

class AuthRepository(ABC):

    @abstractmethod
    async def register_user(self, user_entity:UserDBEntity) -> UserEntity:
        pass

    @abstractmethod
    async def login_user(self, email:str, password:str) -> UserEntity:
        pass