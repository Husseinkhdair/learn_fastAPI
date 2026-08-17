from fastapi import APIRouter, Depends, HTTPException, status

from core.dependencies import provide_login_use_case,provide_register_use_case
from domain.auth.entities.user_entitiy import UserDBEntity
from presentation.auth.schema.login_user_schema import LoginUserSchema
from presentation.auth.schema.register_user_schema import RegisterUserSchema


router = APIRouter(
    prefix="/auth",
    tags=["Auth Controller"]
)

@router.post("/login")
async def login(schema: LoginUserSchema, use_case = Depends(provide_login_use_case)):
    try:
        result = await use_case.execute(schema.email, schema.password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if result.is_success:
        return {"message": "Login successful", "user": result.value}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=result.error)

@router.post("/register")
async def register(schema: RegisterUserSchema, use_case = Depends(provide_register_use_case)):
    try:
        user = UserDBEntity(
            id="generated_id",  # You might want to generate a unique ID here
            name=schema.name,
            age=schema.age,
            email=schema.email,
            password=schema.password,
            is_admin=False,
        )
        result = await use_case.execute(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if result.is_success:
        return {
            "message": "User registered successfully",
            "data": result.value
        }
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error)

