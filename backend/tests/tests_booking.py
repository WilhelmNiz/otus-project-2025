import allure
import pytest
from datetime import date
from backend.models.booking import (
    BookingCreateRequest,
    BookingGetResponse,
    BookingDates
)


@allure.feature("Бронирования")
@allure.story("Базовые операции с бронированиями")
class TestBookingBasicOperations:
    """Базовые тесты операций с бронированиями."""

    def test_get_all_bookings(self, booking_client):
        """Тест: получить список всех существующих бронирований."""
        with allure.step("Запрашиваем все bookingid"):
            booking_ids = booking_client.get_all_bookings()

        with allure.step("Проверяем структуру ответа"):
            assert isinstance(booking_ids, list)
            assert len(booking_ids) >= 10
            assert all(isinstance(id_, int) for id_ in booking_ids)

    def test_get_booking_by_existing_id(self, booking_client):
        """Тест: получить детали бронирования по известному ID."""
        with allure.step("Получаем первый ID из списка"):
            all_ids = booking_client.get_all_bookings()
            first_id = all_ids[0]

        with allure.step(f"Запрашиваем бронирование с ID {first_id}"):
            booking = booking_client.get_booking_by_id(first_id)

        with allure.step("Валидируем структуру ответа"):
            assert isinstance(booking, BookingGetResponse)
            assert isinstance(booking.firstname, str) and booking.firstname
            assert isinstance(booking.lastname, str) and booking.lastname
            assert isinstance(booking.totalprice, int) and booking.totalprice > 0

    def test_get_booking_nonexistent_id(self, booking_client):
        """Тест: запрос бронирования с несуществующим ID."""
        with allure.step("Запрашиваем бронирование с ID 999999"):
            with pytest.raises(Exception, match=r"404|Not Found"):
                booking_client.get_booking_by_id(999999)


@allure.feature("Бронирования")
@allure.story("Фильтрация бронирований")
class TestBookingFiltering:
    """Тесты фильтрации бронирований."""

    @pytest.mark.parametrize("filter_name,filter_value,expected_min_count", [
        ("firstname", "Jim", 1),
        ("lastname", "Brown", 1),
        ("checkin", "2013-01-01", 5),
        ("checkout", "2014-01-01", 5),
    ], ids=["by_firstname", "by_lastname", "by_checkin", "by_checkout"])
    def test_filter_bookings(self, booking_client, filter_name, filter_value, expected_min_count):
        """Параметризованный тест фильтрации бронирований."""
        with allure.step(f"Фильтрация по {filter_name} = {filter_value}"):
            response = booking_client.session.get(
                f"{booking_client.base_url}/booking?{filter_name}={filter_value}"
            )

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            data = response.json()
            assert len(data) >= expected_min_count
            assert all("bookingid" in item for item in data)


@allure.feature("Бронирования")
@allure.story("Создание бронирований")
class TestBookingCreation:
    """Тесты создания бронирований."""

    def test_create_booking_valid_data(self, booking_client):
        """Тест: создание бронирования с валидными данными."""
        payload = BookingCreateRequest(
            firstname="Александр",
            lastname="Смирнов",
            totalprice=250,
            depositpaid=True,
            bookingdates=BookingDates(
                checkin=date(2025, 6, 1),
                checkout=date(2025, 6, 10)
            ),
            additionalneeds="Обед"
        )

        with allure.step("Создание бронирования с валидными данными"):
            booking_id = booking_client.create_booking(payload)

        with allure.step("Проверка созданного бронирования"):
            assert isinstance(booking_id, int) and booking_id > 0

            # Проверяем, что бронирование действительно создалось
            booking = booking_client.get_booking_by_id(booking_id)
            assert booking.firstname == "Александр"
            assert booking.lastname == "Смирнов"

    @pytest.mark.parametrize("payload,expected_error", [
        (
                BookingCreateRequest(
                    firstname="", lastname="Иванов", totalprice=100,
                    depositpaid=True, bookingdates=BookingDates(
                        checkin=date(2025, 9, 1), checkout=date(2025, 9, 5)
                    )
                ),
                r"400|Bad Request"
        ),
        (
                BookingCreateRequest(
                    firstname="Иван", lastname="", totalprice=100,
                    depositpaid=True, bookingdates=BookingDates(
                        checkin=date(2025, 9, 1), checkout=date(2025, 9, 5)
                    )
                ),
                r"400|Bad Request"
        ),
        (
                BookingCreateRequest(
                    firstname="Иван", lastname="Петров", totalprice=-50,
                    depositpaid=True, bookingdates=BookingDates(
                        checkin=date(2025, 9, 1), checkout=date(2025, 9, 5)
                    )
                ),
                r"400|Bad Request"
        ),
    ], ids=["empty_firstname", "empty_lastname", "negative_price"])
    def test_create_booking_invalid_data(self, booking_client, payload, expected_error):
        """Параметризованный тест: создание с невалидными данными."""
        with allure.step("Попытка создания с невалидными данными"):
            with pytest.raises(Exception, match=expected_error):
                booking_client.create_booking(payload)


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