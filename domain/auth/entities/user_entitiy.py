
class UserEntity:
    def __init__(self, id: str, name: str, age: int, is_admin: bool = False):
        self.id = id
        self.name = name
        self.age = age
        self.is_admin = is_admin




class UserDBEntity(UserEntity):
    def __init__(
        self,
        id: str,
        name: str,
        age: int,
        email: str,
        password: str,
        is_admin: bool = False,
    ):
        super().__init__(id=id, name=name, age=age, is_admin=is_admin)
        
        self.email = email
        self.password = password