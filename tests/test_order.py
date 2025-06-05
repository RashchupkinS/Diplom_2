import allure
from data import TestMessages
from helper import User, Order


import requests
from urls import Urls


# класс с тестами для создания заказа
class TestCreateOrder:

    @allure.title('Создание заказа без авторизации пользователя')
    def test_create_order_without_authorization_successful_creation(self, random_ingredients):
        print(random_ingredients)
        payload = {"ingredients": random_ingredients}
        response = Order.create_order(payload)
        assert response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION["code"]
        assert response.json()["success"] == TestMessages.ORDER_SUCCESSFUL_CREATION["success"]
        assert TestMessages.ORDER_SUCCESSFUL_CREATION["message"] in response.json()


    @allure.title('Создание заказа с авторизацией пользователя')
    def test_create_order_with_authorization_successful_creation(self, random_user_data, random_ingredients):
        User.register_user(random_user_data)
        login_response = User.login_user(random_user_data)
        token = User.get_access_token(login_response)
        print(random_ingredients)
        payload = {"headers":token, "ingredients": random_ingredients}
        response = Order.create_order(payload)
        assert response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION["code"]
        assert response.json()["success"] == TestMessages.ORDER_SUCCESSFUL_CREATION["success"]
        assert TestMessages.ORDER_SUCCESSFUL_CREATION["message"] in response.json()


    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_authorization_and_ingredients_not_created(self):
        payload = {"ingredients": {}}
        response = Order.create_order(payload)
        assert response.status_code == TestMessages.ORDER_NOT_CREATED_NO_INGREDIENTS["code"]
        assert response.json()["success"] == TestMessages.ORDER_NOT_CREATED_NO_INGREDIENTS["success"]
        assert response.json()["message"] == TestMessages.ORDER_NOT_CREATED_NO_INGREDIENTS["message"]


    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_without_authorization_and_wrong_ingredients_hash_not_created(self, random_ingredients):
        changed_ingredients = Order.change_ingredients_hash(random_ingredients)
        payload = {"ingredients": changed_ingredients}
        response = Order.create_order(payload)
        assert response.status_code == TestMessages.ORDER_NOT_CREATED_WRONG_HASH["code"]
        assert TestMessages.ORDER_NOT_CREATED_WRONG_HASH["text"] in response.text


class TestGetOrder:

    @allure.title('')
    def test_get_user_order_without_authorization(self):
        response = Order.get_order()
        assert response.status_code == TestMessages.GET_ORDER_NOT_AUTHORIZED_USER["code"]
        assert response.json()["success"] == TestMessages.GET_ORDER_NOT_AUTHORIZED_USER["success"]
        assert response.json()["message"] == TestMessages.GET_ORDER_NOT_AUTHORIZED_USER["message"]


    @allure.title('')
    def test_get_user_order_with_authorization(self, random_user_data):
        User.register_user(random_user_data)
        login_response = User.login_user(random_user_data)
        token = User.get_access_token(login_response)
        header = {'Authorization': token}
        response = requests.get(url=Urls.GET_USER_ORDER, headers=header)
        print(response.json())
        assert response.status_code == TestMessages.GET_ORDER_AUTHORIZED_USER["code"]
        assert response.json()["success"] == TestMessages.GET_ORDER_AUTHORIZED_USER["success"]
        assert TestMessages.GET_ORDER_AUTHORIZED_USER["message"] in response.json()




