import os
from functools import lru_cache
from fastapi import Depends

from data.auth.data_sources.fack_auth_repository import FackAuthRepository
from data.auth.data_sources.mongo_auth_repository import MongoAuthRepository
from data.auth.repository.auth_repositoy_imp import AuthRepositoryImp
from domain.auth.repository.auth_repository import AuthRepository
from domain.auth.usecauses.login_user_usecase import LoginUserUseCase
from domain.auth.usecauses.register_user_usecase import RegisterUserUseCase
from domain.auth.usecauses.refresh_token_usecase import RefreshTokenUseCase


@lru_cache()
def provide_auth_repository() -> AuthRepository:
    use_fake = os.getenv("USE_FAKE_REPO", "false").lower() == "true"
    data_source = FackAuthRepository() if use_fake else MongoAuthRepository()
    return AuthRepositoryImp(data_source=data_source)


# Dependency Injection for Use Cases
def provide_login_use_case(
    repo: AuthRepository = Depends(provide_auth_repository)
) -> LoginUserUseCase:
    return LoginUserUseCase(repo)


def provide_register_use_case(
    repo: AuthRepository = Depends(provide_auth_repository)
) -> RegisterUserUseCase:
    return RegisterUserUseCase(repo)


def provide_refresh_token_use_case() -> RefreshTokenUseCase:
    return RefreshTokenUseCase()
