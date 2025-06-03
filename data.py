email_domains = [
                "@yandex.ru",
                "@gmail.com",
                "@ya.ru",
                "@mail.ru"
]

# класс содержит коды и сообщения ответов на запросы
class TestMessages:

    USER_SUCCESSFUL_CREATION = {"code": 200, "message": True}
    USER_LOGIN_ALREADY_IN_USE = {"code": 403, "message": False}
    USER_NOT_ENOUGH_REGISTER_DATA = {"code": 403, "message": False}
    USER_SUCCESSFUL_AUTHORIZATION = {"code": 200, "message": True}
    USER_NOT_ENOUGH_AUTHORIZATION_DATA = {"code": 401, "message": False}
    USER_ACCOUNT_NOT_FOUND = {"code": 401, "message": False}
    USER_DELETE = {"code": 202, "message": True}
    USER_SUCCESSFUL_EDIT_DATA = {"code": 200, "message": True}
    #
    # ORDER_SUCCESSFUL_CREATION = {"code": 201, "message": "track"}
    # ORDER_GET_LIST_OF_ORDERS = {"code": 200, "message": "orders"}


# переменная содержит параметры которые можно исключить при попытке регистрации без определённого параметра
exclude_register_parameters = ["email", "password", "name"]

# переменная содержит параметры которые можно исключить при попытке авторизации без определённого параметра
exclude_login_parameters = ["email", "password"]

# переменная содержит параметры которые можно изменить при попытке авторизации с изменённым параметром
change_login_parameters = ["email", "password"]

change_authorize_parameters = ["email", "password", "name"]




