from domain.auth.entities.user_entitiy import UserDBEntity
class UserModel(UserDBEntity):
    def __init__(
        self,
        id: str,
        name: str,
        age: int,
        email: str,
        password: str,
        is_admin: bool = False
    ):
        super().__init__(id=id, name=name, age=age, email=email, password=password, is_admin=is_admin)


    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            age=data.get("age"),
            email=data.get("email"),
            password=data.get("password"),
            is_admin=data.get("is_admin", False)
        )
    @classmethod
    def from_entity(cls, user_entity: UserDBEntity):
        return cls(
            id=user_entity.id,
            name=user_entity.name,
            age=user_entity.age,
            email=user_entity.email,
            password=user_entity.password,
            is_admin=user_entity.is_admin
        )
    @classmethod
    def to_dict(cls, user_model):
        return {
            "id": user_model.id,
            "name": user_model.name,
            "age": user_model.age,
            "email": user_model.email,
            "password": user_model.password,
            "is_admin": user_model.is_admin
        }
