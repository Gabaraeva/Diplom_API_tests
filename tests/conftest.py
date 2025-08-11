import pytest
import requests
from pydantic.v1 import BaseModel

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

class UserData(BaseModel):
    email: str
    password: str
    name: str

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def random_user():
    import time
    return UserData(
        email=f"test{int(time.time())}@example.com",
        password="strongPassword123",
        name=f"User{int(time.time())}"
    )

@pytest.fixture
def register_user(base_url, random_user):
    response = requests.post(
        f"{base_url}/auth/register",
        json={
            "email": random_user.email,
            "password": random_user.password,
            "name": random_user.name
        }
    )
    return response.json(), random_user

@pytest.fixture
def auth_token(base_url, register_user):
    _, user_data = register_user
    response = requests.post(
        f"{base_url}/auth/login",
        json={
            "email": user_data.email,
            "password": user_data.password
        }
    )
    return response.json()["accessToken"]

@pytest.fixture
def valid_ingredients(base_url):
    response = requests.get(f"{base_url}/ingredients")
    return [item["_id"] for item in response.json()["data"]][:2]
