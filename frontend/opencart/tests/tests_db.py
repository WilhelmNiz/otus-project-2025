import allure
from helpers.helper_tests_db import (
    create_customer,
    get_customer_by_id,
    update_customer,
    delete_customer
)
from faker import Faker

fake = Faker()


@allure.feature("Работа с клиентами в БД OpenCart")
@allure.story("Создание нового клиента")
def test_create_customer(connection):
    with allure.step("Создаем нового клиента"):
        customer_id = create_customer(connection)

    with allure.step("Проверяем, что клиент создан"):
        customer = get_customer_by_id(connection, customer_id)
        assert customer is not None
        assert customer['customer_id'] == customer_id


@allure.feature("Работа с клиентами в БД OpenCart")
@allure.story("Обновление данных клиента")
def test_update_customer(connection):
    with allure.step("Создаем клиента для теста"):
        customer_id = create_customer(connection)

    with allure.step("Подготавливаем новые данные для обновления"):
        update_data = {
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "email": fake.email(),
            "telephone": fake.phone_number()
        }

    with allure.step("Обновляем данные клиента"):
        result = update_customer(connection, customer_id, update_data)
        assert result is True

    with allure.step("Проверяем обновленные данные"):
        updated_customer = get_customer_by_id(connection, customer_id)
        assert updated_customer['firstname'] == update_data['firstname']
        assert updated_customer['lastname'] == update_data['lastname']
        assert updated_customer['email'] == update_data['email']
        assert updated_customer['telephone'] == update_data['telephone']


@allure.feature("Работа с клиентами в БД OpenCart")
@allure.story("Негативный тест: обновление несуществующего клиента")
def test_update_nonexistent_customer(connection):
    with allure.step("Пытаемся обновить несуществующего клиента"):
        update_data = {
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "email": fake.email(),
            "telephone": fake.phone_number()
        }
        result = update_customer(connection, 999999, update_data)
        assert result is False


@allure.feature("Работа с клиентами в БД OpenCart")
@allure.story("Удаление клиента")
def test_delete_customer(connection):
    with allure.step("Создаем клиента для теста"):
        customer_id = create_customer(connection)

    with allure.step("Удаляем клиента"):
        result = delete_customer(connection, customer_id)
        assert result is True

    with allure.step("Проверяем, что клиент удален"):
        deleted_customer = get_customer_by_id(connection, customer_id)
        assert deleted_customer is None


@allure.feature("Работа с клиентами в БД OpenCart")
@allure.story("Негативный тест: удаление несуществующего клиента")
def test_delete_nonexistent_customer(connection):
    with allure.step("Пытаемся удалить несуществующего клиента"):
        result = delete_customer(connection, 999999)
        assert result is False