from pydantic import BaseModel

class UserInfoDTO(BaseModel):
    id: int
    name: str
    email: str
    age: int
    is_admin: bool = False