import requests
from data.models import UserData
from config import BASE_URL

class UserAPI:
    @staticmethod
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
    def login(user: UserData):
        return requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": user.email,
                "password": user.password
            }
        )

    @staticmethod
    def delete(token: str):
        return requests.delete(
            f"{BASE_URL}/auth/user",
            headers={"Authorization": token}
        )