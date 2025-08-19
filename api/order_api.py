import allure
import requests
from config import BASE_URL

class OrderAPI:
    @staticmethod
    @allure.step("Создать заказ с ингредиентами: {ingredients}")
    def create(ingredients: list, token: str = None):
        headers = {"Authorization": token} if token else {}
        return requests.post(
            f"{BASE_URL}/orders",
            json={"ingredients": ingredients},
            headers=headers
        )

    @staticmethod
    @allure.step("Получить список ингредиентов")
    def get_ingredients():
        response = requests.get(f"{BASE_URL}/ingredients")
        return [item["_id"] for item in response.json()["data"]]