from pydantic import BaseModel, EmailStr, Field


class RegisterUserSchema(BaseModel):
    name: str = Field(..., description="User name",min_length=3, max_length=50)
    age: int = Field(..., description="User age", ge=0, le=120)
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password" ,max_length=20, min_length=8)