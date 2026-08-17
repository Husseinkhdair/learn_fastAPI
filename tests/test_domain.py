import pytest
from data.auth.data_sources.fack_auth_repository import FackAuthRepository
from domain.auth.entities.user_entitiy import UserDBEntity
from domain.auth.usecauses.register_user_usecase import RegisterUserUseCase
from domain.auth.usecauses.login_user_usecase import LoginUserUseCase

@pytest.mark.asyncio
async def test_register_user_usecase():
    repo = FackAuthRepository()
    use_case = RegisterUserUseCase(repo)
    user_db = UserDBEntity(
        id="generated",
        name="Sami",
        age=30,
        email="sami@example.com",
        password="samipassword123",
        is_admin=False
    )
    result = await use_case.execute(user_db)
    assert result.is_success is True
    assert result.value.name == "Sami"

@pytest.mark.asyncio
async def test_login_user_usecase():
    repo = FackAuthRepository()
    reg_use_case = RegisterUserUseCase(repo)
    login_use_case = LoginUserUseCase(repo)

    user_db = UserDBEntity(
        id="generated",
        name="Sami",
        age=30,
        email="sami@example.com",
        password="samipassword123",
        is_admin=False
    )
    await reg_use_case.execute(user_db)

    result = await login_use_case.execute("sami@example.com", "samipassword123")
    assert result.is_success is True
    assert result.value.name == "Sami"
