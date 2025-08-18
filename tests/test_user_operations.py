import allure
import pytest
from data.models import UserData
from data.error_messages import ErrorMessages
from api.user_api import UserAPI

@allure.feature("User Operations")
class TestUserOperations:

    @allure.title("Create unique user")
    def test_create_unique_user(self, random_user):
        response = UserAPI.register(random_user)
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Create user without token")
    def test_create_user_without_token(self, random_user):
        response = UserAPI.register(random_user)
        user_data = response.json()
        assert "accessToken" not in user_data

    @allure.title("Create duplicate user")
    def test_create_duplicate_user(self, register_user):
        _, user_data, _ = register_user
        response = UserAPI.register(user_data)
        assert response.status_code == 403
        assert response.json()["message"] == ErrorMessages.USER_ALREADY_EXISTS

    @allure.title("Create user with missing field")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, random_user, missing_field):
        user_dict = random_user.dict()
        user_dict.pop(missing_field)
        response = UserAPI.register(UserData(**user_dict))
        assert response.status_code == 403
        assert ErrorMessages.REQUIRED_FIELDS in response.json()["message"]

    @allure.title("Login with valid credentials")
    def test_login_valid_user(self, register_user):
        _, credentials, _ = register_user
        response = UserAPI.login(credentials)
        assert response.status_code == 200
        assert "accessToken" in response.json()

    @allure.title("Login with invalid credentials")
    def test_login_invalid_credentials(self):
        response = UserAPI.login(UserData(
            email="invalid@example.com",
            password="wrong",
            name="Invalid"
        ))
        assert response.status_code == 401
        assert ErrorMessages.INCORRECT_CREDENTIALS in response.json()["message"]