# класс содержит ссылки API
class Urls:
    # ссылки для работы с пользователем
    MAIN_URL = 'https://stellarburgers.nomoreparties.site/'
    CREATE_USER = MAIN_URL + '/api/auth/register'
    DELETE_USER = MAIN_URL + '/api/auth/user'
    LOGIN_USER = MAIN_URL + '/api/auth/login'
    EDIT_USER = MAIN_URL + '/api/auth/user'

    # # ссылки для работы с заказом
    CREATE_ORDER = MAIN_URL + '/api/orders'
    INGREDIENTS =  MAIN_URL + '/api/ingredients'
    GET_USER_ORDER = MAIN_URL + '/api/orders'
    # GET_LIST_OF_ORDERS = MAIN_URL + '/api/v1/orders'


