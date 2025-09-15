import time

def measure_response_time(func, *args, **kwargs):
    """Измерение времени выполнения функции."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

def assert_response_time(response_time: float, max_time: float = 2.0):
    """Проверка времени ответа."""
    assert response_time < max_time, f"Время ответа слишком большое: {response_time} секунд"