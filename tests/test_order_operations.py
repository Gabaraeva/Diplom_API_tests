import allure
import pytest
from data.error_messages import ErrorMessages
from api.order_api import OrderAPI

@allure.feature("Order Operations")
class TestOrderOperations:

    @allure.title("Create order with authorization")
    def test_create_order_auth(self, auth_token, valid_ingredients):
        response = OrderAPI.create(valid_ingredients, token=auth_token)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()
        assert "number" in response.json()["order"]

    @allure.title("Create order without authorization")
    def test_create_order_no_auth(self, valid_ingredients):
        response = OrderAPI.create(valid_ingredients)
        assert response.status_code == 401
        assert ErrorMessages.NOT_AUTHORIZED in response.json()["message"]

    @allure.title("Create order without ingredients")
    def test_create_order_no_ingredients(self, auth_token):
        response = OrderAPI.create([], token=auth_token)
        assert response.status_code == 400
        assert ErrorMessages.INGREDIENT_IDS_REQUIRED in response.json()["message"]

    @allure.title("Create order with invalid ingredients")
    def test_create_order_invalid_ingredients(self, auth_token):
        response = OrderAPI.create(["invalid_hash_12345"], token=auth_token)
        assert response.status_code == 500