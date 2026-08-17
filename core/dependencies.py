from functools import lru_cache
from fastapi import Depends

from data.auth.data_sources.fack_auth_repository import FackAuthRepository
from data.auth.repository.auth_repositoy_imp import AuthRepositoryImp
from domain.auth.repository.auth_repository import AuthRepository
from domain.auth.usecauses.login_user_usecase import LoginUserUseCase
from domain.auth.usecauses.register_user_usecase import RegisterUserUseCase



# lru_cache تجعل الـ Fake Repository كائن واحد مشترك طوال تشغيل السيرفر (Singleton)
@lru_cache()
def provide_auth_repository() -> AuthRepository:
    return AuthRepositoryImp(data_source=FackAuthRepository())


# حقن الـ Use Case
def provide_login_use_case(
    repo: AuthRepository = Depends(provide_auth_repository)
) -> LoginUserUseCase:
    return LoginUserUseCase(repo)


def provide_register_use_case(
    repo: AuthRepository = Depends(provide_auth_repository)
) -> RegisterUserUseCase:
    return RegisterUserUseCase(repo)

