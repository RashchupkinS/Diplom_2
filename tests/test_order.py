import allure
import pytest
from data import TestMessages
from helper import Order



# класс с тестами для создания заказа
class TestCreateOrder:

    @allure.title('Создание заказа')
    def test_create_order_successful_creation(self, random_ingredients):
        print(random_ingredients)
        payload = {"ingredients": random_ingredients}

        response = Order.create_order(payload)
        assert response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION["code"]
        assert response.json()["success"] == TestMessages.ORDER_SUCCESSFUL_CREATION["success"]
        assert TestMessages.ORDER_SUCCESSFUL_CREATION["message"] in response.json()
    

