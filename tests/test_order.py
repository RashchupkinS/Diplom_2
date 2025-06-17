import allure
from data import TestMessages
from helper import User, Order



# класс с тестами для создания заказа
class TestCreateOrder:

    @allure.title('Создание заказа без авторизации пользователя')
    def test_create_order_user_not_authorized_successful_creation(self, random_ingredients):
        payload = {"ingredients": random_ingredients}
        response = Order.create_order(payload)
        assert response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION["code"]
        assert response.json()["success"] == TestMessages.ORDER_SUCCESSFUL_CREATION["success"]
        assert TestMessages.ORDER_SUCCESSFUL_CREATION["message"] in response.json()


    @allure.title('Создание заказа с авторизацией пользователя')
    def test_create_order_authorized_user_successful_creation(self, register_user_with_random_user_data, random_ingredients):
        _, random_user_data = register_user_with_random_user_data
        login_response = User.login_user(random_user_data)
        token = User.get_access_token(login_response)
        payload = {"ingredients": random_ingredients}
        response = Order.create_order(payload, token=token)
        assert response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION["code"]
        assert response.json()["success"] == TestMessages.ORDER_SUCCESSFUL_CREATION["success"]
        assert TestMessages.ORDER_SUCCESSFUL_CREATION["message"] in response.json()


    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_authorized_user_order_without_ingredients_not_created(self, register_user_with_random_user_data):
        _, random_user_data = register_user_with_random_user_data
        login_response = User.login_user(random_user_data)
        token = User.get_access_token(login_response)
        payload = {"ingredients": {}}
        response = Order.create_order(payload, token=token)
        assert response.status_code == TestMessages.ORDER_NOT_CREATED_NO_INGREDIENTS["code"]
        assert response.json()["success"] == TestMessages.ORDER_NOT_CREATED_NO_INGREDIENTS["success"]
        assert response.json()["message"] == TestMessages.ORDER_NOT_CREATED_NO_INGREDIENTS["message"]


    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_authorized_user_and_wrong_ingredients_hash_not_created(self,
                                                        register_user_with_random_user_data, random_ingredients):
        _, random_user_data = register_user_with_random_user_data
        login_response = User.login_user(random_user_data)
        token = User.get_access_token(login_response)
        changed_ingredients = Order.change_ingredients_hash(random_ingredients)
        payload = {"ingredients": changed_ingredients}
        response = Order.create_order(payload, token=token)
        assert response.status_code == TestMessages.ORDER_NOT_CREATED_WRONG_HASH["code"]
        assert TestMessages.ORDER_NOT_CREATED_WRONG_HASH["text"] in response.text


# класс с тестами для получения данных по заказу
class TestGetOrder:

    @allure.title('Получение данных заказа пользователя, пользователь не авторизован')
    def test_get_user_order_not_authorized_user(self):
        response = Order.get_users_order()
        assert response.status_code == TestMessages.GET_ORDER_NOT_AUTHORIZED_USER["code"]
        assert response.json()["success"] == TestMessages.GET_ORDER_NOT_AUTHORIZED_USER["success"]
        assert response.json()["message"] == TestMessages.GET_ORDER_NOT_AUTHORIZED_USER["message"]


    @allure.title('Получение данных заказа пользователя, пользователь авторизован')
    def test_get_user_order_authorized_user_order_data_received(self, register_user_with_random_user_data):
        _, random_user_data = register_user_with_random_user_data
        login_response = User.login_user(random_user_data)
        token = User.get_access_token(login_response)
        response = Order.get_users_order(token=token)
        assert response.status_code == TestMessages.GET_ORDER_AUTHORIZED_USER["code"]
        assert response.json()["success"] == TestMessages.GET_ORDER_AUTHORIZED_USER["success"]
        assert TestMessages.GET_ORDER_AUTHORIZED_USER["message"] in response.json()


