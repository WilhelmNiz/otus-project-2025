import allure
import pytest
from datetime import date, timedelta
from backend.models.booking import (
    BookingCreateRequest,
    BookingDates
)


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
        payload = BookingCreateRequest(
            firstname=firstname,
            lastname=lastname,
            totalprice=100,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin=date.today(),
                checkout=date.today() + timedelta(days=7)
            )
        )

        booking_id = booking_client.create_booking(payload)
        booking = booking_client.get_booking_by_id(booking_id)

        assert booking.firstname == firstname
        assert booking.lastname == lastname

    @pytest.mark.parametrize("price", [100, 999, 2500, 1], ids=["minimal", "medium", "high", "minimum"])
    def test_create_booking_different_prices(self, booking_client, price):
        """Тест: создание бронирований с разными ценами."""
        payload = BookingCreateRequest(
            firstname="Test",
            lastname="User",
            totalprice=price,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin=date.today(),
                checkout=date.today() + timedelta(days=3)
            )
        )

        booking_id = booking_client.create_booking(payload)
        booking = booking_client.get_booking_by_id(booking_id)

        assert booking.totalprice == price

    @pytest.mark.parametrize("deposit", [True, False], ids=["with_deposit", "without_deposit"])
    def test_create_booking_deposit_options(self, booking_client, deposit):
        """Тест: создание бронирований с разными вариантами депозита."""
        payload = BookingCreateRequest(
            firstname="Deposit",
            lastname="Test",
            totalprice=200,
            depositpaid=deposit,
            bookingdates=BookingDates(
                checkin=date.today(),
                checkout=date.today() + timedelta(days=5)
            )
        )

        booking_id = booking_client.create_booking(payload)
        booking = booking_client.get_booking_by_id(booking_id)

        assert booking.depositpaid == deposit


@pytest.mark.booking
@pytest.mark.backend
@allure.feature("Бронирования")
@allure.story("Тесты дат бронирований")
class TestBookingDatesScenarios:
    """Тесты различных сценариев с датами."""

    def test_create_booking_same_day_checkin_checkout(self, booking_client):
        """Тест: создание бронирования с одинаковыми датами заезда/выезда."""
        same_date = date.today()

        payload = BookingCreateRequest(
            firstname="Same",
            lastname="Day",
            totalprice=100,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin=same_date,
                checkout=same_date
            )
        )

        booking_id = booking_client.create_booking(payload)
        booking = booking_client.get_booking_by_id(booking_id)

        assert booking.bookingdates.checkin == same_date
        assert booking.bookingdates.checkout == same_date

    def test_create_booking_long_stay(self, booking_client):
        """Тест: создание длительного бронирования."""
        payload = BookingCreateRequest(
            firstname="Long",
            lastname="Stay",
            totalprice=1000,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin=date.today(),
                checkout=date.today() + timedelta(days=30)
            )
        )

        booking_id = booking_client.create_booking(payload)
        booking = booking_client.get_booking_by_id(booking_id)

        assert (booking.bookingdates.checkout - booking.bookingdates.checkin).days == 30


@pytest.mark.booking
@pytest.mark.backend
@allure.feature("Бронирования")
@allure.story("Обновление бронирований")
class TestBookingUpdates:
    """Тесты обновления бронирований."""

    def test_full_update_booking(self, booking_client, auth_token):
        """Тест: полное обновление бронирования."""
        # Сначала создаем тестовое бронирование
        payload = BookingCreateRequest(
            firstname="Тест",
            lastname="Юзер",
            totalprice=100,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin=date(2025, 1, 1),
                checkout=date(2025, 1, 5)
            )
        )
        booking_id = booking_client.create_booking(payload)

        update_payload = BookingCreateRequest(
            firstname="Обновленный",
            lastname="Юзер",
            totalprice=200,
            depositpaid=False,
            bookingdates=BookingDates(
                checkin=date(2025, 2, 1),
                checkout=date(2025, 2, 5)
            ),
            additionalneeds="Завтрак"
        )

        with allure.step("Полное обновление бронирования"):
            updated = booking_client.update_booking_full(booking_id, auth_token, update_payload)

        with allure.step("Проверка обновленных данных"):
            assert updated.firstname == "Обновленный"
            assert updated.totalprice == 200
            assert not updated.depositpaid

    def test_partial_update_booking(self, booking_client, auth_token):
        """Тест: частичное обновление бронирования."""
        # Создаем тестовое бронирование
        payload = BookingCreateRequest(
            firstname="Частичный",
            lastname="Тест",
            totalprice=150,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin=date(2025, 3, 1),
                checkout=date(2025, 3, 5)
            )
        )
        booking_id = booking_client.create_booking(payload)

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


@pytest.mark.booking
@pytest.mark.backend
@allure.feature("Бронирования")
@allure.story("Удаление бронирований")
class TestBookingDeletion:
    """Тесты удаления бронирований."""

    def test_delete_booking(self, booking_client, auth_token):
        """Тест: успешное удаление бронирования."""
        # Создаем бронирование для удаления
        payload = BookingCreateRequest(
            firstname="ДляУдаления",
            lastname="Тест",
            totalprice=100,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin=date(2025, 4, 1),
                checkout=date(2025, 4, 5)
            )
        )
        booking_id = booking_client.create_booking(payload)

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
