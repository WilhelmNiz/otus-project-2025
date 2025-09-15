import pytest
import allure
import random
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FFoptions
from selenium.webdriver.chrome.options import Options as CHoptions
from backend.clients.auth_client import AuthClient
from backend.clients.booking_client import BookingClient


def pytest_addoption(parser):
    parser.addoption("--browser", help="Browser to run tests")
    parser.addoption("--headless", action="store_true", help="Activate headless mode")
    parser.addoption("--url", "-U", help="Base application url", default="http://192.168.31.202:8081/")
    parser.addoption("--remote", action="store_true", help="Use remote Selenoid driver")
    parser.addoption("--remote_url", help="Selenoid hub URL", default="http://localhost:4444/wd/hub")
    parser.addoption("--enable_vnc", action="store_true", help="Enable VNC for remote sessions")
    parser.addoption("--browser_version", help="Browser version for remote sessions", default="128.0")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    url = request.config.getoption("--url")
    is_remote = request.config.getoption("--remote")
    remote_url = request.config.getoption("--remote_url")
    enable_vnc = request.config.getoption("--enable_vnc")
    browser_version = request.config.getoption("--browser_version")

    if is_remote:
        # Настройка для Selenoid
        capabilities = {
            "browserName": "chrome" if browser_name in ["ch", "chrome"] else "firefox",
            "version": browser_version,
            "enableVNC": enable_vnc,
        }

        if browser_name in ["ch", "chrome"]:
            options = CHoptions()
            options.set_capability("selenoid:options", capabilities)
            try:
                driver = webdriver.Remote(
                    command_executor=remote_url,
                    options=options
                )
            except Exception as e:
                print(f"Не удалось запустить Chrome {browser_version}, пробуем 127.0: {e}")
                capabilities["version"] = "127.0"
                options = CHoptions()
                options.set_capability("selenoid:options", capabilities)
                driver = webdriver.Remote(
                    command_executor=remote_url,
                    options=options
                )
        elif browser_name in ["ff", "firefox"]:
            options = FFoptions()
            options.set_capability("selenoid:options", capabilities)
            driver = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )
    else:
        # Локальный запуск
        if browser_name in ["ch", "chrome"]:
            options = CHoptions()
            if headless:
                options.add_argument("headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(f"--user-data-dir=/tmp/chrome_{random.randint(1, 10000)}")
            driver = webdriver.Chrome(options=options)
        elif browser_name in ["ff", "firefox"]:
            options = FFoptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)

    request.addfinalizer(driver.quit)

    def open(path=""):
        return driver.get(url + path.lstrip('/'))

    def go_to_home():
        return driver.get(url)

    driver.open = open
    driver.go_to_home = go_to_home

    try:
        driver.maximize_window()
    except Exception as e:
        print(f"Не удалось максимизировать окно: {e}")
        driver.set_window_size(1920, 1080)

    driver.implicitly_wait(5)

    driver.go_to_home()

    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser")
        if driver is not None:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(
                    driver.page_source,
                    name="page_source",
                    attachment_type=allure.attachment_type.HTML
                )
            except Exception as e:
                print(f"Не удалось сделать скриншот: {e}")


@pytest.fixture(scope="session")
def base_url():
    return "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def api_session():
    """Сессия requests с общими заголовками"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    return session


@pytest.fixture(scope="session")
def auth_client(base_url, api_session) -> AuthClient:
    """Page Object для авторизации"""
    return AuthClient(base_url, api_session)


@pytest.fixture(scope="session")
def booking_client(base_url, api_session) -> BookingClient:
    """Page Object для бронирований"""
    return BookingClient(base_url, api_session)


@pytest.fixture(scope="session")
def auth_token(auth_client) -> str:
    """Получаем токен через клиент"""
    return auth_client.create_token()
