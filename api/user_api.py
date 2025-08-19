import allure
import requests
from data.models import UserData
from config import BASE_URL

class UserAPI:
    @staticmethod
    @allure.step("Зарегистрировать пользователя: {user.email}")
    def register(user: UserData):
        return requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": user.email,
                "password": user.password,
                "name": user.name
            }
        )

    @staticmethod
    @allure.step("Выполнить вход пользователя: {user.email}")
    def login(user: UserData):
        return requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": user.email,
                "password": user.password
            }
        )

    @staticmethod
    @allure.step("Удалить пользователя")
    def delete(token: str):
        return requests.delete(
            f"{BASE_URL}/auth/user",
            headers={"Authorization": token}
        )