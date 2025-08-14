# tests/test_user_operations.py
import allure
import requests
import pytest
from config import BASE_URL
from tests.models import UserData
from tests.error_messages import ErrorMessages


@allure.feature("User Operations")
class TestUserOperations:

    @allure.title("Create unique user")
    def test_create_unique_user(self, base_url, random_user):
        with allure.step("Register new user"):
            response = requests.post(
                f"{base_url}/auth/register",
                json={
                    "email": random_user.email,
                    "password": random_user.password,
                    "name": random_user.name
                }
            )

        with allure.step("Check successful registration"):
            assert response.status_code == 200
            assert response.json()["success"] is True

        # Удаление пользователя после теста
        token = response.json().get("accessToken", "")
        if token:
            requests.delete(
                f"{base_url}/auth/user",
                headers={"Authorization": token}
            )

    @allure.title("Create duplicate user")
    def test_create_duplicate_user(self, base_url, register_user):
        _, user_data = register_user

        with allure.step("Try to register same user again"):
            response = requests.post(
                f"{base_url}/auth/register",
                json={
                    "email": user_data.email,
                    "password": user_data.password,
                    "name": user_data.name
                }
            )

        with allure.step("Check duplicate error"):
            assert response.status_code == 403
            assert response.json()["message"] == ErrorMessages.USER_ALREADY_EXISTS

    @allure.title("Create user with missing field")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, base_url, random_user, missing_field):
        user_data = {
            "email": random_user.email,
            "password": random_user.password,
            "name": random_user.name
        }
        user_data.pop(missing_field)

        with allure.step(f"Register without {missing_field}"):
            response = requests.post(
                f"{base_url}/auth/register",
                json=user_data
            )

        with allure.step("Check validation error"):
            assert response.status_code == 403
            assert ErrorMessages.REQUIRED_FIELDS in response.json()["message"]

    @allure.title("Login with valid credentials")
    def test_login_valid_user(self, base_url, register_user):
        _, user_data = register_user

        with allure.step("Perform login"):
            response = requests.post(
                f"{base_url}/auth/login",
                json={
                    "email": user_data.email,
                    "password": user_data.password
                }
            )

        with allure.step("Check successful login"):
            assert response.status_code == 200
            assert "accessToken" in response.json()

    @allure.title("Login with invalid credentials")
    def test_login_invalid_credentials(self, base_url):
        with allure.step("Attempt login with wrong credentials"):
            response = requests.post(
                f"{base_url}/auth/login",
                json={
                    "email": "invalid@example.com",
                    "password": "wrong"
                }
            )

        with allure.step("Check authentication error"):
            assert response.status_code == 401
            assert ErrorMessages.INCORRECT_CREDENTIALS in response.json()["message"]