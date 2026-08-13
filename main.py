from datetime import timedelta

from fastapi import Depends, FastAPI
from Schemas.ProductSchema import ProductSchema
from functions.get_current_user import get_current_user
from functions.jwt import create_access_token
from models.product_model import Product
from models.user_model import User
from Schemas.user_register_schema import UserRegisterSchema
from DTOs.user_info_dto import UserInfoDTO
from functions.security import hash_password, verify_password
from controllers.auth_controller import router as auth_router

app = FastAPI()
app.include_router(auth_router)







@app.get("/")
def read_root():
    return {"Hello": "World"}







# @app.get("/users/")
# async def get_users(current_user: UserInfoDTO = Depends(get_current_user)):
#     return current_user