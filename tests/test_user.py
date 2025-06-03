import allure
import pytest
from helper import User
from data import TestMessages, exclude_parameters #EXCLUDE_PARAMETERS#, CHANGE_PARAMETERS




# класс с тестами для регистрации курьера
class TestCreateUser:

    @allure.title('Создание пользователя')
    def test_create_user_successful_creation(self, random_user_data):
        response = User.register_user(random_user_data)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_CREATION["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_CREATION["message"]


    @allure.title('Нельзя создать двух одинаковых пользователей')
    def test_create_two_identical_users_user_not_created(self, random_user_data):
        User.register_user(random_user_data)
        response = User.register_user(random_user_data)
        assert response.status_code == TestMessages.USER_LOGIN_ALREADY_IN_USE["code"]
        assert response.json()["success"] == TestMessages.USER_LOGIN_ALREADY_IN_USE["message"]


    @pytest.mark.parametrize("parameter", exclude_parameters)
    @allure.title(f'Регистрация пользователя - json не содержит поля - {exclude_parameters}')
    def test_create_user_without_email_field_not_created(self, random_user_data, parameter):
        payload = User.excludes_parameter_from_user_registration_data(random_user_data,
                                                                            exclude=parameter)
        response = User.register_user(payload)
        assert response.status_code == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["message"]

