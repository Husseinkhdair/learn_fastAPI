from abc import ABC, abstractmethod
from core import Result
from domain.auth.entities.user_entitiy import UserEntity

class AuthRepository(ABC):

    @abstractmethod
    async def register_user(self, user_entity:UserEntity) -> Result[UserEntity]:
        pass

    @abstractmethod
    async def login_user(self, email:str, password:str) -> Result[UserEntity]:
        pass