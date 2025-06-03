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
    # COURIER_NOT_ENOUGH_AUTHORIZATION_DATA = {"code": 400, "message": "Недостаточно данных для входа"}
    # COURIER_ACCOUNT_NOT_FOUND = {"code": 404, "message": "Учетная запись не найдена"}
    USER_DELETE = {"code": 202, "message": True}
    #
    # ORDER_SUCCESSFUL_CREATION = {"code": 201, "message": "track"}
    # ORDER_GET_LIST_OF_ORDERS = {"code": 200, "message": "orders"}


# переменная содержит параметры которые можно исключить при попытке регистрации без определённого параметра
EXCLUDE_PARAMETERS = {
    "email": "email",
    "password": "password",
    "name": "name"
}


# переменная содержит параметры которые можно исключить при попытке регистрации без определённого параметра
exclude_parameters = ["email",
                      "password",
                      "name"
]
