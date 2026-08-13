from datetime import timedelta

from fastapi import APIRouter, status
from DTOs.user_info_dto import UserInfoDTO
from Schemas.user_register_schema import UserRegisterSchema
from functions.jwt import create_access_token
from functions.security import hash_password
from models.user_model import User
router = APIRouter(
    prefix="/auth",
    tags=["Auth Controller"]
)

users = []



@router.post("/login")
def login():
    return {"message": "Login success"}


@router.post("/register/")
async def register_user(user: UserRegisterSchema):
    try:
        new_user = user.model_dump()
        new_user["password"] = hash_password(new_user["password"])
        profile = User(**new_user, id=len(users) + 1)
        users.append(profile)
        user_info = UserInfoDTO(**profile.model_dump())
        token = create_access_token(data=user_info)
        refresh_token = create_access_token(data=user_info, expires_delta=timedelta(days=30))
        return {"user": user_info, "access_token": token ,"refresh_token": refresh_token}
    except Exception as e:
        return {"error": str(e)}