import random
import pytest
import allure
from helper import Generator, User, Order



# фикстура генерирует случайные данные пользователя, передаёт их в тест и удаляет пользователя после теста
@pytest.fixture()
def random_user_data():
    with allure.step('Создание случайных регистрационных данных пользователя'):
        random_user_data = Generator.generate_payload()
        yield random_user_data
        User.delete_user(random_user_data)

# фикстура генерирует случайные данные пользователя, передаёт их в тест и удаляет пользователя после теста
@pytest.fixture()
def random_user_data_2():
    with allure.step('Создание случайных регистрационных данных пользователя'):
        random_user_data_2= Generator.generate_payload()
        yield random_user_data_2
        User.delete_user(random_user_data_2)


# фикстура генерирует случайный список из трёх ингредиентов
@pytest.fixture()
def random_ingredients():
    with allure.step('Создание случайного списка из трёх ингредиентов'):
        ingredients = Order.get_ingredients()
        random_ingredient_1 = random.choice(ingredients)
        random_ingredient_2 = random.choice(ingredients)
        random_ingredient_3 = random.choice(ingredients)
        return [random_ingredient_1["_id"],
                random_ingredient_2["_id"],
                random_ingredient_3["_id"]
        ]


