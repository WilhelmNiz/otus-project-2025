from pydantic import BaseModel, RootModel, field_serializer
from datetime import date
from typing import List

class BookingDates(BaseModel):
    checkin: date
    checkout: date

    @field_serializer('checkin', 'checkout')
    def serialize_dates(self, value: date) -> str:
        return value.isoformat()

class BookingCreateRequest(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str = ""

class BookingDetails(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str = ""

class BookingCreateResponse(BaseModel):
    bookingid: int
    booking: BookingDetails

class BookingGetResponse(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str = ""

class BookingIdItem(BaseModel):
    bookingid: int

class BookingListResponseItem(RootModel):
    root: List[BookingIdItem]

class BookingUpdateResponse(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str = ""