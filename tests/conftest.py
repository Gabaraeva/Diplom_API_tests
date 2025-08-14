# tests/conftest.py
import pytest
import requests
import time
from config import BASE_URL
from tests.models import UserData
from tests.error_messages import ErrorMessages


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def random_user():
    return UserData(
        email=f"test{int(time.time())}@example.com",
        password="strongPassword123",
        name=f"User{int(time.time())}"
    )


@pytest.fixture
def register_user(base_url, random_user):
    # Регистрация пользователя
    response = requests.post(
        f"{base_url}/auth/register",
        json={
            "email": random_user.email,
            "password": random_user.password,
            "name": random_user.name
        }
    )
    user_data = response.json()
    token = user_data.get("accessToken", "")

    yield user_data, random_user

    # Финализатор: удаление пользователя после использования
    if token:
        requests.delete(
            f"{base_url}/auth/user",
            headers={"Authorization": token}
        )


@pytest.fixture
def auth_token(register_user):
    user_data, credentials = register_user
    token = user_data.get("accessToken", "")
    if not token:
        # Если токен не получен, авторизуемся
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": credentials.email,
                "password": credentials.password
            }
        )
        token = response.json()["accessToken"]

    yield token

    # Финализатор: удаление пользователя
    requests.delete(
        f"{BASE_URL}/auth/user",
        headers={"Authorization": token}
    )


@pytest.fixture
def valid_ingredients(base_url):
    response = requests.get(f"{base_url}/ingredients")
    return [item["_id"] for item in response.json()["data"]][:2]
