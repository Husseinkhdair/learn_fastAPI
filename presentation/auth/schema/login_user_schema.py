from pydantic import BaseModel,Field, EmailStr


class LoginUserSchema(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password" ,max_length=20, min_length=8)