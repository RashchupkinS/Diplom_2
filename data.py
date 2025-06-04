email_domains = [
                "@yandex.ru",
                "@gmail.com",
                "@ya.ru",
                "@mail.ru"
]

# класс содержит коды и сообщения ответов на запросы
class TestMessages:

    USER_SUCCESSFUL_CREATION = {"code": 200, "success": True, "message": "accessToken"}
    USER_LOGIN_ALREADY_IN_USE = {"code": 403, "success": False, "message": "User already exists"}
    USER_NOT_ENOUGH_REGISTER_DATA = {"code": 403, "success": False, "message": "Email, password and name are required fields"}
    USER_SUCCESSFUL_AUTHORIZATION = {"code": 200, "success": True, "message": "accessToken"}
    USER_NOT_ENOUGH_AUTHORIZATION_DATA = {"code": 401, "success": False, "message": "email or password are incorrect"}
    USER_ACCOUNT_NOT_FOUND = {"code": 401, "success": False, "message": "email or password are incorrect"}
    USER_DELETE = {"code": 202, "success": True, "message": "User successfully removed"}
    USER_SUCCESSFUL_UPDATE_DATA = {"code": 200, "success": True, "message": "user"}
    USER_DO_NOT_UPDATE_DATA_NOT_AUTHORIZED = {"code": 401, "success": False, "message": "You should be authorised"}
    USER_DO_NOT_UPDATE_DATA_DUPLICATE_EMAIL = {"code": 403, "success": False, "message": "User with such email already exists"}
    #
    ORDER_SUCCESSFUL_CREATION = {"code": 200, "success": True, "message": "order"}
    # ORDER_GET_LIST_OF_ORDERS = {"code": 200, "message": "orders"}


# переменная содержит параметры которые можно исключить при попытке регистрации без определённого параметра
exclude_register_parameters = ["email", "password", "name"]

# переменная содержит параметры которые можно исключить при попытке авторизации без определённого параметра
exclude_login_parameters = ["email", "password"]

# переменная содержит параметры которые можно изменить при попытке авторизации с изменённым параметром
change_login_parameters = ["email", "password"]

change_authorize_parameters = ["email", "password", "name"]







