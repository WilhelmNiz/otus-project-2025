from datetime import date
from backend.models.booking import BookingGetResponse, BookingUpdateResponse

def assert_booking_created_correctly(booking: BookingGetResponse, expected_data: dict):
    """Проверка корректности создания бронирования."""
    assert booking.firstname == expected_data["firstname"]
    assert booking.lastname == expected_data["lastname"]
    assert booking.totalprice == expected_data["totalprice"]
    assert booking.depositpaid == expected_data["depositpaid"]
    assert booking.bookingdates.checkin == expected_data["checkin"]
    assert booking.bookingdates.checkout == expected_data["checkout"]
    if "additionalneeds" in expected_data:
        assert booking.additionalneeds == expected_data["additionalneeds"]

def assert_booking_updated_correctly(booking: BookingUpdateResponse, expected_data: dict):
    """Проверка корректности обновления бронирования."""
    assert booking.firstname == expected_data["firstname"]
    assert booking.lastname == expected_data["lastname"]
    assert booking.totalprice == expected_data["totalprice"]
    assert booking.depositpaid == expected_data["depositpaid"]
    assert booking.bookingdates.checkin == expected_data["checkin"]
    assert booking.bookingdates.checkout == expected_data["checkout"]
    assert booking.additionalneeds == expected_data["additionalneeds"]

def assert_booking_dates_duration(booking: BookingGetResponse, expected_days: int):
    """Проверка длительности бронирования."""
    actual_days = (booking.bookingdates.checkout - booking.bookingdates.checkin).days
    assert actual_days == expected_days, f"Expected {expected_days} days, got {actual_days}"

def assert_booking_dates_equal(booking: BookingGetResponse, expected_date: date):
    """Проверка одинаковых дат заезда/выезда."""
    assert booking.bookingdates.checkin == expected_date
    assert booking.bookingdates.checkout == expected_date