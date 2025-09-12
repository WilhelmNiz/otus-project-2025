import logging
import requests
from backend.models.auth import AuthRequest, AuthResponse
import allure


class AuthClient:
    """Page Object для авторизации /auth"""

    def __init__(self, base_url: str, session: requests.Session):
        self.base_url = base_url
        self.session = session
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_token(self, username: str = "admin", password: str = "password123") -> str:
        """
        Создает токен аутентификации.

        :return: Возвращает токен в виде строки.
        """
        with allure.step(f"Создание токена для пользователя {username}"):
            self.logger.info(f"Создание токена для пользователя: {username}")

            with allure.step("Подготовка payload"):
                payload = AuthRequest(username=username, password=password)
                self.logger.info(f"Подготовка запроса с данными: {payload.model_dump()}")

            with allure.step("Отправка POST запроса"):
                url = f"{self.base_url}/auth"
                self.logger.info(f"Отправка POST запроса на: {url}")
                response = self.session.post(url, json=payload.model_dump())

            with allure.step("Обработка ответа"):
                self.logger.info(f"Получен ответ: статус {response.status_code}, JSON {response.json()}")

                if response.status_code >= 400:
                    error_data = response.json()
                    if 'reason' in error_data:
                        raise Exception(f"Ошибка аутентификации: {error_data['reason']}")
                    response.raise_for_status()

                token_data = AuthResponse.model_validate(response.json())
                self.logger.info(f"Токен успешно создан")

                return token_data.token