from datetime import date, timedelta
from backend.models.booking import BookingCreateRequest, BookingDates


def create_booking_payload(
        firstname: str = "Test",
        lastname: str = "User",
        totalprice: int = 100,
        depositpaid: bool = True,
        checkin: date = None,
        checkout: date = None,
        additionalneeds: str = "",
        days_delta: int = 7
) -> BookingCreateRequest:
    """Фабрика для создания payload бронирования."""
    if checkin is None:
        checkin = date.today()
    if checkout is None:
        checkout = checkin + timedelta(days=days_delta)

    return BookingCreateRequest(
        firstname=firstname,
        lastname=lastname,
        totalprice=totalprice,
        depositpaid=depositpaid,
        bookingdates=BookingDates(
            checkin=checkin,
            checkout=checkout
        ),
        additionalneeds=additionalneeds
    )


def create_update_payload(
        firstname: str = "Updated",
        lastname: str = "User",
        totalprice: int = 200,
        depositpaid: bool = False,
        checkin: date = None,
        checkout: date = None,
        additionalneeds: str = "Breakfast"
) -> BookingCreateRequest:
    """Фабрика для создания payload обновления."""
    if checkin is None:
        checkin = date(2025, 2, 1)
    if checkout is None:
        checkout = date(2025, 2, 5)

    return BookingCreateRequest(
        firstname=firstname,
        lastname=lastname,
        totalprice=totalprice,
        depositpaid=depositpaid,
        bookingdates=BookingDates(
            checkin=checkin,
            checkout=checkout
        ),
        additionalneeds=additionalneeds
    )