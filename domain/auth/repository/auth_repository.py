from abc import ABC, abstractmethod
from core import Result
from domain.auth.entities.user_entitiy import UserDBEntity, UserEntity

class AuthRepository(ABC):

    @abstractmethod
    async def register_user(self, user_entity:UserDBEntity) -> Result[UserEntity]:
        pass

    @abstractmethod
    async def login_user(self, email:str, password:str) -> Result[UserEntity]:
        pass