import logging
import requests
import allure
from typing import Dict, Any, List
from backend.models.booking import (
    BookingCreateRequest,
    BookingCreateResponse,
    BookingGetResponse,
    BookingUpdateResponse,
    BookingListResponseItem
)


class BookingClient:
    """Page Object для управления бронированиями"""

    def __init__(self, base_url: str, session: requests.Session):
        self.base_url = base_url
        self.session = session
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_all_bookings(self) -> List[int]:
        """Получить список всех ID бронирований"""
        with allure.step("Получение всех ID бронирований"):
            self.logger.info("Запрос всех booking IDs")

            with allure.step("Отправка GET запроса на /booking"):
                response = self.session.get(f"{self.base_url}/booking")
                data = response.json()
                self.logger.info(f"Получен ответ: статус {response.status_code}, JSON {data}")

            with allure.step("Обработка ответа"):
                response.raise_for_status()
                BookingListResponseItem.model_validate(data)
                booking_ids = [item["bookingid"] for item in data]
                self.logger.info(f"Найдено {len(booking_ids)} бронирований")

                return booking_ids

    def get_booking_by_id(self, booking_id: int) -> BookingGetResponse:
        """Получить конкретное бронирование по ID"""
        with allure.step(f"Получение бронирования по ID {booking_id}"):
            self.logger.info(f"Запрос бронирования с ID: {booking_id}")

            with allure.step("Отправка GET запроса"):
                response = self.session.get(f"{self.base_url}/booking/{booking_id}")
                self.logger.info(f"Получен ответ: статус {response.status_code}")

            with allure.step("Валидация и парсинг ответа"):
                response.raise_for_status()
                booking_data = BookingGetResponse.model_validate(response.json())
                self.logger.info(f"Получены данные бронирования: {booking_data}")

                return booking_data

    def create_booking(self, payload: BookingCreateRequest) -> int:
        """Создать бронирование и вернуть его ID"""
        with allure.step("Создание нового бронирования"):
            self.logger.info(f"Создание бронирования с данными: {payload.model_dump()}")

            with allure.step("Подготовка payload"):
                request_data = payload.model_dump()
                self.logger.info(f"Payload для создания: {request_data}")

            with allure.step("Отправка POST запроса на /booking"):
                response = self.session.post(
                    f"{self.base_url}/booking",
                    json=request_data
                )
                self.logger.info(f"Получен ответ: статус {response.status_code}")

            with allure.step("Обработка ответа создания"):
                response.raise_for_status()
                result = response.json()
                BookingCreateResponse.model_validate(result)
                booking_id = result["bookingid"]
                self.logger.info(f"Бронирование создано успешно, ID: {booking_id}")

                return booking_id

    def update_booking_full(self, booking_id: int, token: str, payload: BookingCreateRequest) -> BookingUpdateResponse:
        """Полное обновление бронирования (PUT)"""
        with allure.step(f"Полное обновление бронирования ID {booking_id}"):
            self.logger.info(f"Полное обновление бронирования {booking_id}")

            with allure.step("Подготовка заголовков с токеном"):
                headers = {"Cookie": f"token={token}"}
                self.logger.info(f"Заголовки запроса: {headers}")

            with allure.step("Подготовка данных для обновления"):
                request_data = payload.model_dump()
                self.logger.info(f"Данные для обновления: {request_data}")

            with allure.step("Отправка PUT запроса"):
                response = self.session.put(
                    f"{self.base_url}/booking/{booking_id}",
                    json=request_data,
                    headers=headers
                )
                self.logger.info(f"Получен ответ: статус {response.status_code}")

            with allure.step("Валидация ответа обновления"):
                response.raise_for_status()
                updated_data = BookingUpdateResponse.model_validate(response.json())
                self.logger.info(f"Бронирование успешно обновлено: {updated_data}")

                return updated_data

    def partial_update_booking(self, booking_id: int, token: str, updates: Dict[str, Any]) -> BookingUpdateResponse:
        """Частичное обновление (PATCH)"""
        with allure.step(f"Частичное обновление бронирования ID {booking_id}"):
            self.logger.info(f"Частичное обновление бронирования {booking_id}")

            with allure.step("Подготовка заголовков с токеном"):
                headers = {"Cookie": f"token={token}"}
                self.logger.info(f"Заголовки запроса: {headers}")

            with allure.step("Подготовка данных для частичного обновления"):
                self.logger.info(f"Обновляемые поля: {updates}")

            with allure.step("Отправка PATCH запроса"):
                response = self.session.patch(
                    f"{self.base_url}/booking/{booking_id}",
                    json=updates,
                    headers=headers
                )
                self.logger.info(f"Получен ответ: статус {response.status_code}")

            with allure.step("Валидация ответа частичного обновления"):
                response.raise_for_status()
                updated_data = BookingUpdateResponse.model_validate(response.json())
                self.logger.info(f"Бронирование частично обновлено: {updated_data}")

                return updated_data

    def delete_booking(self, booking_id: int, token: str) -> bool:
        """Удалить бронирование"""
        with allure.step(f"Удаление бронирования ID {booking_id}"):
            self.logger.info(f"Удаление бронирования с ID: {booking_id}")

            with allure.step("Подготовка заголовков с токеном"):
                headers = {"Cookie": f"token={token}"}
                self.logger.info(f"Заголовки запроса: {headers}")

            with allure.step("Отправка DELETE запроса"):
                response = self.session.delete(
                    f"{self.base_url}/booking/{booking_id}",
                    headers=headers
                )
                self.logger.info(f"Получен ответ: статус {response.status_code}")

            with allure.step("Проверка успешности удаления"):
                response.raise_for_status()
                is_success = response.status_code in [200, 201]
                self.logger.info(f"Удаление {'успешно' if is_success else 'не удалось'}")

                return is_success