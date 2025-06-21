import pytest
import allure
from helper import User
from data import TestMessages, register_parameters, login_parameters
import copy



# класс с тестами для регистрации курьера
class TestCreateUser:

    @allure.title('Создание пользователя')
    def test_create_user_successful_creation(self, register_user_with_random_user_data):
        response, _ = register_user_with_random_user_data
        assert response.status_code == TestMessages.USER_SUCCESSFUL_CREATION["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_CREATION["success"]
        assert TestMessages.USER_SUCCESSFUL_CREATION["message"] in response.json()


    @allure.title('Нельзя создать двух одинаковых пользователей')
    def test_create_two_identical_users_user_not_created(self, register_user_with_random_user_data):
        _, random_user_data = register_user_with_random_user_data
        response = User.register_user(random_user_data)
        assert response.status_code == TestMessages.USER_LOGIN_ALREADY_IN_USE["code"]
        assert response.json()["success"] == TestMessages.USER_LOGIN_ALREADY_IN_USE["success"]
        assert response.json()["message"] == TestMessages.USER_LOGIN_ALREADY_IN_USE["message"]


    @pytest.mark.parametrize("parameter", register_parameters)
    @allure.title('Регистрация пользователя, если не указать один из параметров - поле {parameter}')
    def test_create_user_without_one_of_the_field_not_created(self, random_user_data_2, parameter):
        payload = User.excludes_parameter_from_user_registration_data(random_user_data_2,
                                                                            exclude=parameter)
        response = User.register_user(payload)
        assert response.status_code == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["success"]
        assert response.json()["message"] == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["message"]


# класс с тестами для авторизации пользователя
class TestLoginUser:

    @allure.title('Авторизация пользователя')
    def test_login_user_successful_authorized(self, register_user_with_random_user_data):
        _, random_user_data = register_user_with_random_user_data
        response = User.login_user(random_user_data)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_AUTHORIZATION["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_AUTHORIZATION["success"]
        assert TestMessages.USER_SUCCESSFUL_AUTHORIZATION["message"] in response.json()


    @pytest.mark.parametrize("parameter", login_parameters)
    @allure.title('Авторизация пользователя - json не содержит поля - {parameter}')
    def test_login_user_without_one_of_the_field_not_authorized(self,
                                                    register_user_with_random_user_data, parameter):
        _, random_user_data = register_user_with_random_user_data
        payload = User.excludes_parameter_from_user_registration_data(random_user_data,
                                                                            exclude=parameter)
        response = User.login_user(payload)
        assert response.status_code == TestMessages.USER_NOT_ENOUGH_AUTHORIZATION_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_NOT_ENOUGH_AUTHORIZATION_DATA["success"]
        assert response.json()["message"] == TestMessages.USER_NOT_ENOUGH_AUTHORIZATION_DATA["message"]


    @pytest.mark.parametrize("parameter", login_parameters)
    @allure.title('Авторизация пользователя, если неправильно указать {parameter}')
    def test_user_with_non_existent_email_or_password_not_authorized(self,
                                                    register_user_with_random_user_data, parameter):
        _, random_user_data = register_user_with_random_user_data
        payload = User.change_parameter_value_in_user_registration_data(random_user_data,
                                                                              change=parameter)
        response = User.login_user(payload)
        assert response.status_code == TestMessages.USER_ACCOUNT_NOT_FOUND["code"]
        assert response.json()["success"] == TestMessages.USER_ACCOUNT_NOT_FOUND["success"]
        assert response.json()["message"] == TestMessages.USER_ACCOUNT_NOT_FOUND["message"]


# класс с тестами для изменения данных пользователя
class TestEditUser:

    @pytest.mark.parametrize("parameter", register_parameters)
    @allure.title('Изменение данных пользователя - изменить поле {parameter}, пользователь авторизирован')
    def test_edit_user_data_user_authorized_change_one_field_of_the_data_successful_update(self,
                                                                        register_user_with_random_user_data, parameter):
        _, random_user_data = register_user_with_random_user_data
        random_user_data_for_login = copy.deepcopy(random_user_data)
        login_response = User.login_user(random_user_data_for_login)
        token = User.get_access_token(login_response)
        updated_user_data = User.change_parameter_value_in_user_registration_data(random_user_data,
                                                                                  change=parameter)
        # обновление данных пользователя необходимо для удаления пользователя после теста
        random_user_data.update(updated_user_data)
        response =  User.edit_user(random_user_data,token)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_UPDATE_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_UPDATE_DATA["success"]
        assert TestMessages.USER_SUCCESSFUL_UPDATE_DATA["message"] in response.json()


    @pytest.mark.parametrize("parameter", register_parameters)
    @allure.title('Изменение данных пользователя - исключить поле {parameter}, пользователь авторизирован')
    def test_edit_user_data_authorized_user_without_one_of_the_field_successful_update(self,
                                                                        register_user_with_random_user_data, parameter):
        _, random_user_data = register_user_with_random_user_data
        random_user_data_for_login = copy.deepcopy(random_user_data)
        login_response = User.login_user(random_user_data_for_login)
        token = User.get_access_token(login_response)
        updated_user_data = User.excludes_parameter_from_user_registration_data(random_user_data,
                                                                                exclude=parameter)
        # обновление данных пользователя необходимо для удаления пользователя после теста
        random_user_data.update(updated_user_data)
        response =  User.edit_user(updated_user_data, token)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_UPDATE_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_UPDATE_DATA["success"]
        assert TestMessages.USER_SUCCESSFUL_UPDATE_DATA["message"] in response.json()


    @pytest.mark.parametrize("parameter", register_parameters)
    @allure.title('Изменение данных пользователя - изменить поле {parameter}, пользователь НЕ авторизирован')
    def test_edit_user_data_not_authorized_user_change_one_field_of_the_data_not_updated(self,
                                                register_user_with_random_user_data, parameter):
        _, random_user_data = register_user_with_random_user_data
        updated_user_data = User.change_parameter_value_in_user_registration_data(random_user_data,
                                                                                  change=parameter)
        response =  User.edit_user(updated_user_data)
        assert response.status_code == TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["code"]
        assert response.json()["success"] == TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["success"]
        assert response.json()["message"] == TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["message"]


    @pytest.mark.parametrize("parameter", register_parameters)
    @allure.title('Изменение данных пользователя - исключить поле {parameter}, пользователь НЕ авторизирован')
    def test_edit_user_data_not_authorized_user_without_one_of_the_field_data_not_updated(self,
                                                register_user_with_random_user_data, parameter):
        _, random_user_data = register_user_with_random_user_data
        updated_user_data = User.excludes_parameter_from_user_registration_data(random_user_data,
                                                                                  exclude=parameter)
        response =  User.edit_user(updated_user_data)
        assert response.status_code == TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["code"]
        assert response.json()["success"] == TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["success"]
        assert response.json()["message"] == TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["message"]


    @allure.title('Данные пользователя не изменяются, если новый email есть у существующего пользователя')
    def test_edit_user_data_authorized_user_duplicate_email_data_not_updated(self,
                                            register_user_with_random_user_data, random_user_data_2):
        _, random_user_data = register_user_with_random_user_data
        User.register_user(random_user_data_2)
        random_user_data_for_login = copy.deepcopy(random_user_data)
        login_response = User.login_user(random_user_data_for_login)
        token = User.get_access_token(login_response)
        data_for_update = {
            "email": random_user_data_2["email"],
            "password": random_user_data["password"],
            "name": random_user_data["name"]
        }
        response =  User.edit_user(data_for_update, token)
        assert response.status_code == TestMessages.USER_DO_NOT_UPDATE_DATA_DUPLICATE_EMAIL["code"]
        assert response.json()["success"] == TestMessages.USER_DO_NOT_UPDATE_DATA_DUPLICATE_EMAIL["success"]
        assert response.json()["message"] == TestMessages.USER_DO_NOT_UPDATE_DATA_DUPLICATE_EMAIL["message"]


