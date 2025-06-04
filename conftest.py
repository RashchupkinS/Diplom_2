import random

import pytest
from helper import Generator, User, Order
import copy




# фикстура генерирует случайные данные пользователя, передаёт их в тест и удаляет пользователя после теста
@pytest.fixture()
def random_user_data():
    random_user_data = Generator.generate_payload()
    yield random_user_data
    User.delete_user(random_user_data)


# фикстура генерирует случайные данные заказа, передаёт их в тест и удаляет заказ после теста
@pytest.fixture()
def random_ingredients():
    ingredients = Order.get_ingredients()
    random_ingredient_1 = random.choice(ingredients)
    random_ingredient_2 = random.choice(ingredients)
    random_ingredient_3 = random.choice(ingredients)
    return [random_ingredient_1["_id"],
            random_ingredient_2["_id"],
            random_ingredient_3["_id"]
            ]



# фикстура генерирует случайные данные заказа, передаёт их в тест и удаляет заказ после теста
@pytest.fixture()
def random_order_data():
    random_order_data = Generator.generate_random_order_data()
    yield random_order_data
    Order.delete_order_after_test(random_order_data)