from fastapi import APIRouter, Depends, HTTPException, status

from core.dependencies import (
    provide_login_use_case,
    provide_register_use_case,
    provide_refresh_token_use_case,
)
from core.errors.AuthException import InvalidCredentialsException, UserAlreadyExistsException
from domain.auth.entities.user_entitiy import UserDBEntity
from presentation.auth.schema.login_user_schema import LoginUserSchema
from presentation.auth.schema.register_user_schema import RegisterUserSchema
from presentation.auth.schema.refresh_token_schema import RefreshTokenSchema
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth Controller"]
)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(schema: LoginUserSchema, use_case = Depends(provide_login_use_case)):
    try:
        result = await use_case.execute(schema.email, schema.password)
        if not result.is_success:
            if isinstance(result.error, Exception):
                raise result.error
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(result.error))
    except InvalidCredentialsException as e:
        err_msg = str(e)
        status_code = status.HTTP_400_BAD_REQUEST if err_msg == "User not found" else status.HTTP_401_UNAUTHORIZED
        raise HTTPException(status_code=status_code, detail=err_msg)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {
        "message": "Login successful",
        **result.value
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(schema: RegisterUserSchema, use_case = Depends(provide_register_use_case)):
    try:
        user = UserDBEntity(
            id="generated_id",
            name=schema.name,
            age=schema.age,
            email=schema.email,
            password=schema.password,
            is_admin=False,
        )
        result = await use_case.execute(user)
        if not result.is_success:
            if isinstance(result.error, Exception):
                raise result.error
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(result.error))
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {
        "message": "User registered successfully",
        **result.value
    }


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(schema: RefreshTokenSchema, use_case = Depends(provide_refresh_token_use_case)):
    try:
        result = await use_case.execute(schema.refresh_token)
        if not result.is_success:
            if isinstance(result.error, Exception):
                raise result.error
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(result.error))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {
        "message": "Token refreshed successfully",
        **result.value
    }
