def assert_valid_token(token: str):
    """Проверка валидности токена."""
    assert isinstance(token, str), "Токен должен быть строкой"
    assert len(token) > 0, "Токен не должен быть пустым"
    assert " " not in token, "Токен не должен содержать пробелов"