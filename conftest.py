import pytest
from helper import Generator, User#, Order
import copy




# фикстура генерирует случайные данные пользователя, передаёт их в тест и удаляет пользователя после теста
@pytest.fixture()
def random_user_data():
    random_user_data = Generator.generate_payload()
 #   random_user_data_copy = copy.deepcopy(random_user_data)
    yield random_user_data
  #  User.delete_courier(random_user_data_copy)


# фикстура генерирует случайные данные заказа, передаёт их в тест и удаляет заказ после теста
@pytest.fixture()
def random_order_data():
    random_order_data = Generator.generate_random_order_data()
    yield random_order_data
    Order.delete_order_after_test(random_order_data)