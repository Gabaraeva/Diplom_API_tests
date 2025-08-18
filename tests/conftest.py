import pytest
import time
from data.models import UserData
from api.user_api import UserAPI


@pytest.fixture
def random_user():
    return UserData(
        email=f"test{int(time.time())}@example.com",
        password="strongPassword123",
        name=f"User{int(time.time())}"
    )


@pytest.fixture
def register_user(random_user):
    # Регистрация пользователя
    response = UserAPI.register(random_user)
    user_data = response.json()
    token = user_data.get("accessToken", "")

    yield user_data, random_user, token

    # Финализатор: удаление пользователя
    if token:
        UserAPI.delete(token)


@pytest.fixture
def auth_token(register_user):
    user_data, credentials, token = register_user
    if not token:
        # Авторизуемся если токен не получен
        response = UserAPI.login(credentials)
        token = response.json()["accessToken"]

    yield token

    # Финализатор: удаление пользователя
    UserAPI.delete(token)


@pytest.fixture
def valid_ingredients():
    from api.order_api import OrderAPI
    return OrderAPI.get_ingredients()[:2]