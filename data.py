email_domains = [
                "@yandex.ru",
                "@gmail.com",
                "@ya.ru",
                "@mail.ru"
]

# класс содержит коды и сообщения ответов на запросы

class TestMessages:

    USER_SUCCESSFUL_CREATION = {"code": 200, "message": True}
    # COURIER_LOGIN_ALREADY_IN_USE = {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}
    # COURIER_NOT_ENOUGH_REGISTER_DATA = {"code": 400, "message": "Недостаточно данных для создания учетной записи"}
    # COURIER_SUCCESSFUL_AUTHORIZATION = {"code": 200, "message": None}
    # COURIER_NOT_ENOUGH_AUTHORIZATION_DATA = {"code": 400, "message": "Недостаточно данных для входа"}
    # COURIER_ACCOUNT_NOT_FOUND = {"code": 404, "message": "Учетная запись не найдена"}
    # COURIER_DELETE = {"code": 200, "message": True}
    #
    # ORDER_SUCCESSFUL_CREATION = {"code": 201, "message": "track"}
    # ORDER_GET_LIST_OF_ORDERS = {"code": 200, "message": "orders"}