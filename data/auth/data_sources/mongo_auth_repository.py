import uuid
from typing import Optional
from pymongo.database import Database
from core.database import get_database
from core.errors.AuthException import ErrorDataBaseException, InvalidCredentialsException, UserAlreadyExistsException
from core.functions.security import verify_password
from domain.auth.entities.user_entitiy import UserDBEntity, UserEntity
from domain.auth.repository.auth_repository import AuthRepository



class MongoAuthRepository(AuthRepository):
    def __init__(self, database: Optional[Database] = None):
        self.db = database if database is not None else get_database()
        self.collection = self.db["users"]

    async def register_user(self, user_entity: UserDBEntity) -> UserEntity:
        try:
            
    
            try:
                existing_user = self.collection.find_one({"email": user_entity.email})
            except Exception as e:
                raise ErrorDataBaseException(message=str(e))

            if existing_user:
                raise UserAlreadyExistsException()

            # Generate unique ID if needed
            user_id = user_entity.id if user_entity.id and user_entity.id != "generated_id" else str(uuid.uuid4())

            user_doc = {
                "_id": user_id,
                "name": user_entity.name,
                "age": user_entity.age,
                "email": user_entity.email,
                "password": user_entity.password,
                "is_admin": user_entity.is_admin
            }
            try:
                self.collection.insert_one(user_doc)
            except Exception as e:
                raise ErrorDataBaseException(message=str(e))


            created_user = UserEntity(
                id=user_id,
                name=user_entity.name,
                age=user_entity.age,
                is_admin=user_entity.is_admin
            )
            return created_user
        except Exception as e:
            raise

    async def login_user(self, email: str, password: str) -> UserEntity:
        try:
            try:
                user_doc = self.collection.find_one({"email": email})
                if user_doc is None:
                    raise InvalidCredentialsException("User not found")
            except InvalidCredentialsException as e:
                raise
            except Exception as e:
                raise ErrorDataBaseException(message=str(e))

            try:
                stored_hashed_password = user_doc.get("password", "")
                if verify_password(password, stored_hashed_password):
                    user_id = str(user_doc.get("_id") or user_doc.get("id"))
                    user_entity = UserEntity(
                        id=user_id,
                        name=user_doc.get("name"),
                        age=user_doc.get("age"),
                        is_admin=user_doc.get("is_admin", False)
                    )
                    return user_entity
                else:
                    raise InvalidCredentialsException("Invalid email or password")
            except Exception as e:
                raise 
        except Exception as e:
            return 

