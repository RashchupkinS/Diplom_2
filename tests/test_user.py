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
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_CREATION["success"]
        assert TestMessages.USER_SUCCESSFUL_CREATION["message"] in response.json()


    @allure.title('Нельзя создать двух одинаковых пользователей')
    def test_create_two_identical_users_user_not_created(self, random_user_data):
        User.register_user(random_user_data)
        response = User.register_user(random_user_data)
        assert response.status_code == TestMessages.USER_LOGIN_ALREADY_IN_USE["code"]
        assert response.json()["success"] == TestMessages.USER_LOGIN_ALREADY_IN_USE["success"]
        assert response.json()["message"] == TestMessages.USER_LOGIN_ALREADY_IN_USE["message"]


    @pytest.mark.parametrize("parameter", exclude_register_parameters)
    @allure.title(f'Регистрация пользователя - json не содержит поля - {exclude_register_parameters}')
    def test_create_user_without_one_of_the_field_not_created(self, random_user_data, parameter):
        payload = User.excludes_parameter_from_user_registration_data(random_user_data,
                                                                            exclude=parameter)
        response = User.register_user(payload)
        assert response.status_code == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["success"]
        assert response.json()["message"] == TestMessages.USER_NOT_ENOUGH_REGISTER_DATA["message"]


# класс с тестами для авторизации пользователя
class TestLoginUser:

    @allure.title('Авторизация пользователя')
    def test_login_user_successful_authorized(self, random_user_data):
        User.register_user(random_user_data)
        response = User.login_user(random_user_data)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_AUTHORIZATION["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_AUTHORIZATION["success"]
        assert TestMessages.USER_SUCCESSFUL_AUTHORIZATION["message"] in response.json()


    @pytest.mark.parametrize("parameter", exclude_login_parameters)
    @allure.title(f'Авторизация пользователя - json не содержит поля - {exclude_login_parameters}')
    def test_login_user_without_one_of_the_field_not_authorized(self, random_user_data, parameter):
        User.register_user(random_user_data)
        payload = User.excludes_parameter_from_user_registration_data(random_user_data,
                                                                            exclude=parameter)
        response = User.login_user(payload)
        assert response.status_code == TestMessages.USER_NOT_ENOUGH_AUTHORIZATION_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_NOT_ENOUGH_AUTHORIZATION_DATA["success"]
        assert response.json()["message"] == TestMessages.USER_NOT_ENOUGH_AUTHORIZATION_DATA["message"]


    @pytest.mark.parametrize("parameter", change_login_parameters)
    @allure.title('Авторизация пользователя если неправильно указать {parameter}')
    def test_user_with_non_existent_login_or_password_not_authorized(self, random_user_data, parameter):
        User.register_user(random_user_data)
        payload = User.change_parameter_value_in_user_registration_data(random_user_data,
                                                                              change=parameter)
        response = User.login_user(payload)
        assert response.status_code == TestMessages.USER_ACCOUNT_NOT_FOUND["code"]
        assert response.json()["success"] == TestMessages.USER_ACCOUNT_NOT_FOUND["success"]
        assert response.json()["message"] == TestMessages.USER_ACCOUNT_NOT_FOUND["message"]


# класс с тестами для изменения данных пользователя
class TestEditUser:

    @pytest.mark.parametrize("parameter", change_authorize_parameters)
    @allure.title('Изменение данных пользователя с авторизацией')
    def test_edit_user_data_user_with_authorization_successful_update(self, random_user_data, parameter):
        User.register_user(random_user_data)
        random_user_data_login = copy.deepcopy(random_user_data)
        login_response = User.login_user(random_user_data_login)
        token = User.get_token(login_response)
        updated_user_data = User.change_parameter_value_in_user_registration_data(random_user_data,
                                                                        change=parameter)
        random_user_data.update(updated_user_data)
        response =  User.edit_user(token, random_user_data)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_UPDATE_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_UPDATE_DATA["success"]
        assert TestMessages.USER_SUCCESSFUL_UPDATE_DATA["message"] in response.json()


# по этому тесту задать вопрос

    @pytest.mark.parametrize("parameter", exclude_register_parameters)
    @allure.title('Изменение данных пользователя с авторизацией')
    def test_edit_user_data_with_authorization_without_one_of_the_field_successful_update(self, random_user_data, parameter):
        User.register_user(random_user_data)
        random_user_data_login = copy.deepcopy(random_user_data)
        login_response = User.login_user(random_user_data_login)
        token = User.get_token(login_response)
        updated_user_data = User.excludes_parameter_from_user_registration_data(random_user_data,
                                                                                exclude=parameter)
        response =  User.edit_user(token, updated_user_data)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_UPDATE_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_UPDATE_DATA["success"]
        assert TestMessages.USER_SUCCESSFUL_UPDATE_DATA["message"] in response.json()



# узнать про поведение в тесте

    @pytest.mark.parametrize("parameter", change_authorize_parameters)
    @allure.title('Изменение данных пользователя без авторизации')
    def test_edit_user_data_without_authorization_data_not_updated(self, random_user_data, parameter):
        registration_response = User.register_user(random_user_data)
        token = User.get_token(registration_response)
        updated_user_data = User.change_parameter_value_in_user_registration_data(random_user_data,
                                                                        change=parameter)
        response =  User.edit_user(token, updated_user_data)
        random_user_data.update(updated_user_data)
        print(random_user_data)
        assert response.status_code == TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["code"]
        assert response.json()["success"] == TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["success"]
        assert TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["message"] in response.json()


# узнать поведение и необходимость теста

    @pytest.mark.parametrize("parameter", exclude_register_parameters)
    @allure.title('Изменение данных пользователя без авторизации')
    def test_edit_user_data_without_authorization_without_one_of_the_field_data_not_updated(self, random_user_data, parameter):
        print(random_user_data)
        registration_response = User.register_user(random_user_data)
        token = User.get_token(registration_response)
        updated_user_data = User.excludes_parameter_from_user_registration_data(random_user_data,
                                                                        exclude=parameter)
        print(updated_user_data)
        random_user_data.update(updated_user_data)
        print(random_user_data)
        print(updated_user_data)
        response =  User.edit_user(token, updated_user_data)
        print(updated_user_data)
        print(random_user_data)
        assert response.status_code == TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["code"]
        assert response.json()["success"] == TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["success"]
        assert TestMessages.USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED["message"] in response.json()



    @allure.title('Изменение данных пользователя если ввести повторно email')
    def test_edit_user_data_authorized_user_duplicate_email_data_not_updated(self, random_user_data):
        User.register_user(random_user_data)
        print(random_user_data)
        random_user_data_login = copy.deepcopy(random_user_data)
        login_response = User.login_user(random_user_data_login)
        token = User.get_token(login_response)
        print(random_user_data)
        response =  User.edit_user(token, random_user_data)
        assert response.status_code == TestMessages.USER_DO_NOT_UPDATE_DATA_DUPLICATE_EMAIL["code"]
        assert response.json()["success"] == TestMessages.USER_DO_NOT_UPDATE_DATA_DUPLICATE_EMAIL["success"]
        assert TestMessages.USER_DO_NOT_UPDATE_DATA_DUPLICATE_EMAIL["message"] in response.json()




