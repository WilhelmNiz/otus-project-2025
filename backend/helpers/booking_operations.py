import allure
from backend.factories.booking_factory import create_booking_payload

def create_test_booking(booking_client, **kwargs):
    """Создание тестового бронирования с allure steps."""
    with allure.step("Создание тестового бронирования"):
        payload = create_booking_payload(**kwargs)
        booking_id = booking_client.create_booking(payload)
        return booking_id, payload

def create_and_get_booking(booking_client, **kwargs):
    """Создание бронирования и получение его данных."""
    booking_id, payload = create_test_booking(booking_client, **kwargs)
    booking = booking_client.get_booking_by_id(booking_id)
    return booking_id, payload, booking