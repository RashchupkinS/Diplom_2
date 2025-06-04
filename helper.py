import copy

import requests
import allure
import random
import string
from urls import Urls
from faker import Faker
from data import email_domains, TestMessages #  color_selection, ,,




# класс содержит генераторы случайных валидных данных
class Generator:

    # статический метод генерирует случайную последовательность английских букв в нижнем регистре
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string


    # # статический метод генерирует случайную последовательность русских букв в нижнем регистре
    # @staticmethod
    # def generate_random_russian_string(length):
    #     letters = [chr(i) for i in range(1072, 1105)]
    #     random_string = ''.join(random.choice(letters) for _ in range(length))
    #     return random_string


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


    # # статический метод генерирует заказ со случайными валидными данными
    # @staticmethod
    # def generate_random_order_data():
    #     faker = Faker(locale="ru_RU")
    #     order_data = {
    #         "firstName": Generator.generate_random_russian_string(10),
    #         "lastName": Generator.generate_random_russian_string(15),
    #         "address": Generator.generate_random_russian_string(20),
    #         "metroStation": faker.random_int(min=1, max=10, step=1),
    #         "phone": f"8{Generator.generate_random_numbers_as_string(10)}",
    #         "rentTime": faker.random_int(min=1, max=6, step=1),
    #         "deliveryDate": faker.date_between(start_date='+1d', end_date='+5d').isoformat(),
    #         "comment": Generator.generate_random_russian_string(5),
    #         "color": random.choice(color_selection)
    #     }
    #     return order_data


# класс содержит методы для работы с пользователем
class User:

    # статический метод регистрирует нового курьера
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


    # статический метод авторизует курьера
    @staticmethod
    @allure.step('Авторизация пользователя')
    def login_user(registered_user_data):
        registered_user_data_for_login = copy.deepcopy(registered_user_data)
        del registered_user_data_for_login["name"]
        response = requests.post(url=Urls.LOGIN_USER, json=registered_user_data_for_login)
        return response


    # статический метод изменяет данные курьера
    @staticmethod
    @allure.step('Авторизация пользователя')
    def edit_user(token, changed_data_of_registered_user):
        header = {'Authorization': token}
        response = requests.patch(url=Urls.EDIT_USER, headers=header, json=changed_data_of_registered_user)
        return response


    # статический метод удаляет курьера после теста
    @staticmethod
    @allure.step('Удаление пользователя')
    def delete_user(registered_user_data):
        response = User.login_user(registered_user_data)
        if response.status_code == TestMessages.USER_SUCCESSFUL_AUTHORIZATION["code"]:
            token = response.json()["accessToken"]
            header = {'Authorization': token}
            a1 = requests.delete(Urls.DELETE_USER, headers=header)
            # print(registered_user_data)
            print(a1.status_code, a1.json())


    @staticmethod
    def get_token(response):
        return response.json()["accessToken"]


# # класс содержит методы для работы с заказом
# class Order:
#
#     # статический метод создаёт заказ
#     # и добавляет к json трек заказа по ключу DELETE для дальнейшего удаления заказа после теста
#     @staticmethod
#     @allure.step('Создать заказ')
#     def create_order(order_data):
#         response = requests.post(url=Urls.CREATE_ORDER, json=order_data)
#         if response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION["code"]:
#             order_data["delete"] = response.json()["track"]
#         return response
#
#
#     # статический метод удаляет заказ после теста
#     @staticmethod
#     def delete_order_after_test(order_data):
#         track = order_data["delete"]
#         requests.put(url=Urls.CANCEL_ORDER, json={
#             "track": track
#         })
#
#
#     # статический метод получает список заказов
#     @staticmethod
#     @allure.step('Получить список заказов')
#     def get_list_of_orders():
#         return requests.get(url=Urls.GET_LIST_OF_ORDERS)



