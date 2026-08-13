from pydantic import  BaseModel, Field

class UserRegisterSchema(BaseModel):
    name: str = Field(
        ...,
         min_length=2,
           max_length=100,
             description="The name of the user")
    email: str = Field(..., max_length=100, description="The email of the user")
    password: str = Field(
        ...,
        min_length=8,
        max_length=72, 
        description="Password must be between 8 and 72 characters",
    )
    age: int = Field(..., gt=0, description="The age of the user")