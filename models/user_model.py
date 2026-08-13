from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    age: int
    is_admin: Optional[bool] = False
