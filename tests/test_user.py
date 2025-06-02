import allure
from helper import User
from data import TestMessages#, EXCLUDE_PARAMETERS, CHANGE_PARAMETERS




# класс с тестами для регистрации курьера
class TestCreateUser:

    @allure.title('Создание курьера')
    def test_create_user_successful_creation(self, random_user_data):
        response = User.register_user(random_user_data)
        print(response.status_code)
        print(response.json())
        assert response.status_code == TestMessages.USER_SUCCESSFUL_CREATION["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_CREATION["message"]


    @allure.title('Нельзя создать двух одинаковых пользователей')
    def test_create_two_identical_users_user_not_created(self, random_user_data):
        User.register_courier(random_user_data)
        response = User.register_user(random_courier_data)
        assert response.status_code == TestMessages.USER_LOGIN_ALREADY_IN_USE["code"]
        assert response.json()["message"] == TestMessages.USER_LOGIN_ALREADY_IN_USE["message"]


    @allure.title('Регистрация пользователя - json не содержит поля - email')
    def test_create_user_without_email_field_not_created(self, random_user_data):
        payload = User.excludes_parameter_from_courier_registration_data(random_courier_data,
                                                                            exclude=EXCLUDE_PARAMETERS["login"])
        response = User.register_user(payload)
        assert response.status_code == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["code"]
        assert response.json()["message"] == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["message"]


    @allure.title('Регистрация пользователя - json не содержит поля - password')
    def test_create_user_without_password_field_not_created(self, random_user_data):
        payload = User.excludes_parameter_from_courier_registration_data(random_courier_data,
                                                                            exclude=EXCLUDE_PARAMETERS["password"])
        response = User.register_user(payload)
        assert response.status_code == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["code"]
        assert response.json()["message"] == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["message"]


    @allure.title('Регистрация пользователя - json не содержит поля - name')
    def test_create_user_without_name_field_successful_created(self, random_user_data):
        payload = User.excludes_parameter_from_courier_registration_data(random_courier_data,
                                                                            exclude=EXCLUDE_PARAMETERS["firstName"])
        response = User.register_user(payload)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_CREATION["code"]
        assert response.json()["ok"] == TestMessages.USER_SUCCESSFUL_CREATION["message"]