import requests
from config import BASE_URL

class OrderAPI:
    @staticmethod
    def create(ingredients: list, token: str = None):
        headers = {"Authorization": token} if token else {}
        return requests.post(
            f"{BASE_URL}/orders",
            json={"ingredients": ingredients},
            headers=headers
        )

    @staticmethod
    def get_ingredients():
        response = requests.get(f"{BASE_URL}/ingredients")
        return [item["_id"] for item in response.json()["data"]