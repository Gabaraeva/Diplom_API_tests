import allure
import requests
import pytest

@allure.feature("Order Operations")
class TestOrderOperations:
    
    @allure.title("Create order with authorization")
    def test_create_order_auth(self, base_url, auth_token, valid_ingredients):
        headers = {"Authorization": auth_token}
        
        with allure.step("Create order with valid ingredients"):
            response = requests.post(
                f"{base_url}/orders",
                json={"ingredients": valid_ingredients},
                headers=headers
            )
        
        with allure.step("Check successful order creation"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Create order without authorization")
    def test_create_order_no_auth(self, base_url, valid_ingredients):
        with allure.step("Create order without token"):
            response = requests.post(
                f"{base_url}/orders",
                json={"ingredients": valid_ingredients}
            )
        
        with allure.step("Check order created successfully"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Create order with valid ingredients")
    def test_create_order_with_ingredients(self, base_url, auth_token, valid_ingredients):
        headers = {"Authorization": auth_token}
        
        with allure.step("Create order with ingredients"):
            response = requests.post(
                f"{base_url}/orders",
                json={"ingredients": valid_ingredients},
                headers=headers
            )
        
        with allure.step("Check order details"):
            assert response.status_code == 200
            assert "order" in response.json()
            assert "number" in response.json()["order"]

    @allure.title("Create order without ingredients")
    def test_create_order_no_ingredients(self, base_url, auth_token):
        headers = {"Authorization": auth_token}
        
        with allure.step("Attempt to create empty order"):
            response = requests.post(
                f"{base_url}/orders",
                json={},
                headers=headers
            )
        
        with allure.step("Check validation error"):
            assert response.status_code == 400
            assert "Ingredient ids must be provided" in response.json()["message"]

    @allure.title("Create order with invalid ingredients")
    def test_create_order_invalid_ingredients(self, base_url, auth_token):
        headers = {"Authorization": auth_token}
        
        with allure.step("Create order with fake ingredients"):
            response = requests.post(
                f"{base_url}/orders",
                json={"ingredients": ["invalid_hash_12345"]},
                headers=headers
            )
        
        with allure.step("Check server error"):
            assert response.status_code == 500
