import copy
import requests
import allure
import random
import string
from urls import Urls
from data import email_domains, TestMessages




# класс содержит генераторы случайных валидных данных
class Generator:

    # статический метод генерирует случайную последовательность английских букв в нижнем регистре
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string


    # статический метод генерирует случайную последовательность цифр в формате строки
    @staticmethod
    def generate_random_numbers_as_string(length):
        numbers = '0123456789'
        random_numbers = ''.join(random.choice(numbers) for _ in range(length))
        return random_numbers


    # статический метод генерирует случайную последовательность цифр в формате строки
    @staticmethod
    def generate_random_email_domain():
        random_domain = random.choice(email_domains)
        return random_domain


    # статический метод генерирует список из валидных случайных: почты, пароля и имени
    @staticmethod
    def generate_payload():
        email = (Generator.generate_random_string(5) +
                 Generator.generate_random_numbers_as_string(3) +
                 Generator.generate_random_email_domain())
        password = Generator.generate_random_string(6) + Generator.generate_random_numbers_as_string(3)
        name = Generator.generate_random_string(5)
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        return payload


# класс содержит методы для работы с пользователем
class User:

    # статический метод регистрирует нового пользователя
    @staticmethod
    @allure.step('Регистрация пользователя')
    def register_user(user_data):
        response = requests.post(url=Urls.CREATE_USER, json=user_data)
        return response


    # статический метод исключает заданную пару ключ-значение из регистрационных данных
    @staticmethod
    def excludes_parameter_from_user_registration_data(registered_user_data, exclude):
        data_copy = copy.deepcopy(registered_user_data)
        del data_copy[exclude]
        return data_copy


    # статический метод изменяет значение регистрационных данных по ключу(исключает последний символ)
    @staticmethod
    def change_parameter_value_in_user_registration_data(registered_user_data, change):
        data_copy = copy.deepcopy(registered_user_data)
        data_copy[change] = data_copy[change][:-1]
        return data_copy


    # статический метод авторизует пользователя
    @staticmethod
    @allure.step('Авторизация пользователя')
    def login_user(registered_user_data):
        registered_user_data_for_login = copy.deepcopy(registered_user_data)
        del registered_user_data_for_login["name"]
        response = requests.post(url=Urls.LOGIN_USER, json=registered_user_data_for_login)
        return response


    # статический метод изменяет данные пользователя
    @staticmethod
    @allure.step('Авторизация пользователя')
    def edit_user(token, changed_data_of_registered_user):
        header = {'Authorization': token}
        response = requests.patch(url=Urls.EDIT_USER, headers=header, json=changed_data_of_registered_user)
        return response


    # статический метод удаляет пользователя после теста
    @staticmethod
    @allure.step('Удаление пользователя')
    def delete_user(registered_user_data):
        response = User.login_user(registered_user_data)
        if response.status_code == TestMessages.USER_SUCCESSFUL_AUTHORIZATION["code"]:
            token = response.json()["accessToken"]
            header = {'Authorization': token}
            a1 = requests.delete(Urls.DELETE_USER, headers=header)

            print(a1.status_code, a1.json())


    @staticmethod
    def get_access_token(response):
        return response.json()["accessToken"]


# класс содержит методы для работы с заказом
class Order:

    # статический метод создаёт заказ
    @staticmethod
    @allure.step('Создать заказ')
    def create_order(order_data):
        response = requests.post(url=Urls.CREATE_ORDER, json=order_data)
        return response


    @staticmethod
    @allure.step('Получение списка ингредиентов')
    def get_ingredients():
        response = requests.get(Urls.INGREDIENTS)
        return response.json()['data']


    @staticmethod
    @allure.step('Изменение хеша ингредиентов')
    def change_ingredients_hash(ingredients):
        return [item[:-1] for item in ingredients]


    # статический метод создаёт заказ
    @staticmethod
    @allure.step('')
    def get_order():
        response = requests.get(url=Urls.GET_USER_ORDER)
        return response

