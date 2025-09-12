import allure
import pytest
import time


@allure.feature("Аутентификация")
@allure.story("Успешное создание токена")
def test_create_token_success(auth_client):
    """Тест: успешная аутентификация с корректными данными."""
    with allure.step("Вызываем create_token() с параметрами по умолчанию"):
        token = auth_client.create_token()

    with allure.step("Проверяем, что токен — непустая строка"):
        assert isinstance(token, str)
        assert len(token) > 0
        assert " " not in token


@allure.feature("Аутентификация")
@allure.story("Неуспешная аутентификация - параметризованные тесты")
@pytest.mark.parametrize("username,password,test_name", [
    ("wrong_user", "wrong_pass", "неверные учетные данные"),
    ("", "password123", "пустой логин"),
    ("admin", "", "пустой пароль"),
    ("nonexistent", "test123", "несуществующий пользователь"),
    ("admin", "short", "короткий пароль"),
    ("a" * 100, "password123", "очень длинный логин"),
])
def test_create_token_negative_cases(auth_client, username, password, test_name):
    """Параметризованный тест: различные сценарии неуспешной аутентификации."""
    with allure.step(f"Тестируем случай: {test_name}"):
        with allure.step(f"Подготавливаем данные: логин='{username}', пароль='{password}'"):
            pass

        with allure.step("Отправляем запрос с некорректными данными"):
            with pytest.raises(Exception, match=r"Bad credentials"):
                auth_client.create_token(username=username, password=password)


@allure.feature("Аутентификация")
@allure.story("Безопасность: попытка SQL-инъекции")
@pytest.mark.parametrize("username,password,injection_type", [
    ("admin", "' OR '1'='1' --", "обход пароля через OR"),
    ("' OR 1=1 --", "password123", "обход логина через OR"),
    ("admin", "' UNION SELECT NULL --", "UNION-атака"),
    ("admin", "'; DROP TABLE users; --", "инъекция с DROP"),
    ("admin", "' OR 'a'='a", "базовая инъекция"),
    ("", "' OR ''='", "инъекция с пустыми полями"),
])
def test_auth_sql_injection_attempt(auth_client, username, password, injection_type):
    """Параметризованный тест: попытка SQL-инъекции в поля авторизации."""
    with allure.step(f"Тестируем тип инъекции: {injection_type}"):
        with allure.step(f"Пробуем SQL-инъекцию: логин='{username}', пароль='{password}'"):
            with pytest.raises(Exception, match=r"Bad credentials"):
                auth_client.create_token(username=username, password=password)


@allure.feature("Аутентификация")
@allure.story("Ошибка: неверный Content-Type")
def test_create_token_wrong_content_type(auth_client, api_session):
    """Тест: отправка с неверным Content-Type."""
    with allure.step("Сохраняем оригинальные заголовки сессии"):
        original_headers = api_session.headers.copy()

    with allure.step("Меняем Content-Type на text/plain"):
        api_session.headers["Content-Type"] = "text/plain"

    with allure.step("Отправляем запрос с неверным Content-Type"):
        with pytest.raises(Exception, match=r"Bad credentials"):
            auth_client.create_token()

    with allure.step("Восстанавливаем оригинальные заголовки"):
        api_session.headers.update(original_headers)


@allure.feature("Аутентификация")
@allure.story("Время ответа API")
def test_auth_response_time(auth_client):
    """Тест: проверка времени ответа сервера."""
    with allure.step(f"Замеряем время выполнения запроса"):
        start_time = time.time()
        token = auth_client.create_token()
        end_time = time.time()

    with allure.step("Проверяем время ответа и валидность токена"):
        response_time = end_time - start_time
        assert response_time < 2.0, f"Время ответа слишком большое: {response_time} секунд"
        assert isinstance(token, str) and len(token) > 0