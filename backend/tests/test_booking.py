import allure
import pytest
from datetime import date, timedelta

from backend.factories.booking_factory import create_booking_payload, create_update_payload
from backend.helpers.booking_helpers import (
    assert_booking_created_correctly,
    assert_booking_updated_correctly,
    assert_booking_dates_duration,
    assert_booking_dates_equal
)
from backend.helpers.booking_operations import create_and_get_booking


@pytest.mark.booking
@pytest.mark.backend
@allure.feature("Бронирования")
@allure.story("Базовые операции с бронированиями")
class TestBookingBasicOperations:
    """Базовые тесты операций с бронированиями."""

    def test_get_all_bookings(self, booking_client):
        """Тест: получить список всех существующих бронирований."""
        with allure.step("Запрашиваем все bookingid"):
            booking_client.get_all_bookings()

    def test_get_booking_by_existing_id(self, booking_client):
        """Тест: получить детали бронирования по известному ID."""
        with allure.step("Получаем первый ID из списка"):
            all_ids = booking_client.get_all_bookings()
            first_id = all_ids[0]

        with allure.step(f"Запрашиваем бронирование с ID {first_id}"):
            booking_client.get_booking_by_id(first_id)

    def test_get_booking_nonexistent_id(self, booking_client):
        """Тест: запрос бронирования с несуществующим ID."""
        with allure.step("Запрашиваем бронирование с ID 999999"):
            with pytest.raises(Exception, match=r"404|Not Found"):
                booking_client.get_booking_by_id(999999)


@pytest.mark.booking
@pytest.mark.backend
@allure.feature("Бронирования")
@allure.story("Параметризованное создание бронирований")
class TestParameterizedBookingCreation:
    """Параметризованные тесты создания бронирований."""

    @pytest.mark.parametrize("firstname,lastname", [
        ("John", "Doe"),
        ("Мария", "Иванова"),
        ("Jean", "Dupont"),
        ("Анна", "Schmidt"),
    ], ids=["english", "russian", "french", "german"])
    def test_create_booking_different_names(self, booking_client, firstname, lastname):
        """Тест: создание бронирований с разными именами."""
        with allure.step("Подготовка payload с разными именами"):
            payload = create_booking_payload(
                firstname=firstname,
                lastname=lastname,
                totalprice=100
            )

        with allure.step("Создание бронирования"):
            booking_id = booking_client.create_booking(payload)

        with allure.step("Получение созданного бронирования"):
            booking = booking_client.get_booking_by_id(booking_id)

        with allure.step("Проверка корректности данных бронирования"):
            expected_data = {
                "firstname": firstname,
                "lastname": lastname,
                "totalprice": 100,
                "depositpaid": True,
                "checkin": date.today(),
                "checkout": date.today() + timedelta(days=7)
            }
            assert_booking_created_correctly(booking, expected_data)

    @pytest.mark.parametrize("price", [100, 999, 2500, 1], ids=["minimal", "medium", "high", "minimum"])
    def test_create_booking_different_prices(self, booking_client, price):
        """Тест: создание бронирований с разными ценами."""
        with allure.step("Подготовка payload с разными ценами"):
            payload = create_booking_payload(
                firstname="Test",
                lastname="User",
                totalprice=price,
                days_delta=3
            )

        with allure.step("Создание бронирования"):
            booking_id = booking_client.create_booking(payload)

        with allure.step("Получение созданного бронирования"):
            booking = booking_client.get_booking_by_id(booking_id)

        with allure.step("Проверка корректности цены"):
            expected_data = {
                "firstname": "Test",
                "lastname": "User",
                "totalprice": price,
                "depositpaid": True,
                "checkin": date.today(),
                "checkout": date.today() + timedelta(days=3)
            }
            assert_booking_created_correctly(booking, expected_data)

    @pytest.mark.parametrize("deposit", [True, False], ids=["with_deposit", "without_deposit"])
    def test_create_booking_deposit_options(self, booking_client, deposit):
        """Тест: создание бронирований с разными вариантами депозита."""
        with allure.step("Подготовка payload с разными опциями депозита"):
            payload = create_booking_payload(
                firstname="Deposit",
                lastname="Test",
                totalprice=200,
                depositpaid=deposit,
                days_delta=5
            )

        with allure.step("Создание бронирования"):
            booking_id = booking_client.create_booking(payload)

        with allure.step("Получение созданного бронирования"):
            booking = booking_client.get_booking_by_id(booking_id)

        with allure.step("Проверка корректности опции депозита"):
            expected_data = {
                "firstname": "Deposit",
                "lastname": "Test",
                "totalprice": 200,
                "depositpaid": deposit,
                "checkin": date.today(),
                "checkout": date.today() + timedelta(days=5)
            }
            assert_booking_created_correctly(booking, expected_data)


@pytest.mark.booking
@pytest.mark.backend
@allure.feature("Бронирования")
@allure.story("Тесты дат бронирований")
class TestBookingDatesScenarios:
    """Тесты различных сценариев с датами."""

    def test_create_booking_same_day_checkin_checkout(self, booking_client):
        """Тест: создание бронирования с одинаковыми датами заезда/выезда."""
        same_date = date.today()

        with allure.step("Подготовка payload с одинаковыми датами"):
            payload = create_booking_payload(
                firstname="Same",
                lastname="Day",
                totalprice=100,
                checkin=same_date,
                checkout=same_date
            )

        with allure.step("Создание бронирования"):
            booking_id = booking_client.create_booking(payload)

        with allure.step("Получение созданного бронирования"):
            booking = booking_client.get_booking_by_id(booking_id)

        with allure.step("Проверка одинаковых дат заезда/выезда"):
            assert_booking_dates_equal(booking, same_date)

    def test_create_booking_long_stay(self, booking_client):
        """Тест: создание длительного бронирования."""
        with allure.step("Подготовка payload для длительного проживания"):
            payload = create_booking_payload(
                firstname="Long",
                lastname="Stay",
                totalprice=1000,
                days_delta=30
            )

        with allure.step("Создание бронирования"):
            booking_id = booking_client.create_booking(payload)

        with allure.step("Получение созданного бронирования"):
            booking = booking_client.get_booking_by_id(booking_id)

        with allure.step("Проверка длительности бронирования"):
            assert_booking_dates_duration(booking, 30)


@pytest.mark.booking
@pytest.mark.backend
@allure.feature("Бронирования")
@allure.story("Обновление бронирований")
class TestBookingUpdates:
    """Тесты обновления бронирований."""

    def test_full_update_booking(self, booking_client, auth_token):
        """Тест: полное обновление бронирования."""
        with allure.step("Создание тестового бронирования"):
            booking_id, original_payload, original_booking = create_and_get_booking(
                booking_client,
                firstname="Тест",
                lastname="Юзер",
                totalprice=100,
                checkin=date(2025, 1, 1),
                checkout=date(2025, 1, 5)
            )

        with allure.step("Подготовка данных для полного обновления"):
            update_payload = create_update_payload(
                firstname="Обновленный",
                lastname="Юзер",
                totalprice=200,
                depositpaid=False,
                checkin=date(2025, 2, 1),
                checkout=date(2025, 2, 5),
                additionalneeds="Завтрак"
            )

        with allure.step("Полное обновление бронирования"):
            updated = booking_client.update_booking_full(booking_id, auth_token, update_payload)

        with allure.step("Проверка обновленных данных"):
            expected_data = {
                "firstname": "Обновленный",
                "lastname": "Юзер",
                "totalprice": 200,
                "depositpaid": False,
                "checkin": date(2025, 2, 1),
                "checkout": date(2025, 2, 5),
                "additionalneeds": "Завтрак"
            }
            assert_booking_updated_correctly(updated, expected_data)

    def test_partial_update_booking(self, booking_client, auth_token):
        """Тест: частичное обновление бронирования."""
        with allure.step("Создание тестового бронирования"):
            booking_id, original_payload, original_booking = create_and_get_booking(
                booking_client,
                firstname="Частичный",
                lastname="Тест",
                totalprice=150,
                checkin=date(2025, 3, 1),
                checkout=date(2025, 3, 5)
            )

        with allure.step("Подготовка данных для частичного обновления"):
            updates = {
                "firstname": "НовоеИмя",
                "lastname": "НоваяФамилия",
                "additionalneeds": "Ужин"
            }

        with allure.step("Частичное обновление бронирования"):
            updated = booking_client.partial_update_booking(booking_id, auth_token, updates)

        with allure.step("Проверка обновленных полей"):
            assert updated.firstname == "НовоеИмя"
            assert updated.lastname == "НоваяФамилия"
            assert updated.additionalneeds == "Ужин"

            assert updated.totalprice == original_booking.totalprice
            assert updated.depositpaid == original_booking.depositpaid
            assert updated.bookingdates.checkin == original_booking.bookingdates.checkin
            assert updated.bookingdates.checkout == original_booking.bookingdates.checkout


@pytest.mark.booking
@pytest.mark.backend
@allure.feature("Бронирования")
@allure.story("Удаление бронирований")
class TestBookingDeletion:
    """Тесты удаления бронирований."""

    def test_delete_booking(self, booking_client, auth_token):
        """Тест: успешное удаление бронирования."""
        with allure.step("Создание бронирования для удаления"):
            booking_id, payload, booking = create_and_get_booking(
                booking_client,
                firstname="ДляУдаления",
                lastname="Тест",
                totalprice=100,
                checkin=date(2025, 4, 1),
                checkout=date(2025, 4, 5)
            )

        with allure.step("Удаление бронирования"):
            result = booking_client.delete_booking(booking_id, auth_token)

        with allure.step("Проверка успешности удаления"):
            assert result is True

        with allure.step("Проверка, что бронирование удалено"):
            with pytest.raises(Exception, match=r"404|Not Found"):
                booking_client.get_booking_by_id(booking_id)

    def test_delete_nonexistent_booking(self, booking_client, auth_token):
        """Тест: попытка удалить несуществующее бронирование."""
        with allure.step("Попытка удаления несуществующего бронирования"):
            with pytest.raises(Exception, match=r"405|Method Not Allowed|404"):
                booking_client.delete_booking(999999, auth_token)