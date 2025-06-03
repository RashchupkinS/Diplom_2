import allure
import pytest
from helper import User
from data import (TestMessages, exclude_register_parameters, exclude_login_parameters,
                  change_login_parameters, change_authorize_parameters)
import copy




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


    @pytest.mark.parametrize("parameter", exclude_register_parameters)
    @allure.title(f'Регистрация пользователя - json не содержит поля - {exclude_register_parameters}')
    def test_create_user_without_one_of_the_field_not_created(self, random_user_data, parameter):
        payload = User.excludes_parameter_from_user_registration_data(random_user_data,
                                                                            exclude=parameter)
        response = User.register_user(payload)
        assert response.status_code == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["message"]


# класс с тестами для авторизации пользователя
class TestLoginUser:

    @allure.title('Авторизация пользователя')
    def test_login_user_successful_authorized(self, random_user_data):
        User.register_user(random_user_data)
        response = User.login_user(random_user_data)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_AUTHORIZATION["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_AUTHORIZATION["message"]


    @pytest.mark.parametrize("parameter", exclude_login_parameters)
    @allure.title(f'Авторизация пользователя - json не содержит поля - {exclude_login_parameters}')
    def test_login_user_without_one_of_the_field_not_authorized(self, random_user_data, parameter):
        User.register_user(random_user_data)
        payload = User.excludes_parameter_from_user_registration_data(random_user_data,
                                                                            exclude=parameter)
        response = User.login_user(payload)
        assert response.status_code == TestMessages.USER_NOT_ENOUGH_AUTHORIZATION_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_NOT_ENOUGH_AUTHORIZATION_DATA["message"]


    @pytest.mark.parametrize("parameter", change_login_parameters)
    @allure.title('Авторизация пользователя если неправильно указать {parameter}')
    def test_user_with_non_existent_login_or_password_not_authorized(self, random_user_data, parameter):
        User.register_user(random_user_data)
        payload = User.change_parameter_value_in_user_registration_data(random_user_data,
                                                                              change=parameter)
        response = User.login_user(payload)
        assert response.status_code == TestMessages.USER_ACCOUNT_NOT_FOUND["code"]
        assert response.json()["success"] == TestMessages.USER_ACCOUNT_NOT_FOUND["message"]


# класс с тестами для изменения данных пользователя
class TestEditUser:

    @pytest.mark.parametrize("parameter", change_authorize_parameters)
    @allure.title('Изменение данных пользователя с авторизацией')
    def test_edit_user_data_user_with_authorization_successful_change(self, random_user_data, parameter):
        User.register_user(random_user_data)
        random_user_data_copy = copy.deepcopy(random_user_data)
        User.login_user(random_user_data)
        payload = User.change_parameter_value_in_user_registration_data(random_user_data_copy,
                                                                        change=parameter)
        response =  User.edit_authorized_user(random_user_data_copy, payload)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_EDIT_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_EDIT_DATA["message"]



