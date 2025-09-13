import allure
import pytest
from frontend.page_object.catalog_page import CatalogPage
from frontend.page_object.admin_page import AdminPage


@pytest.mark.ui
@pytest.mark.admin
@allure.feature("Администрирование OpenCart")
@allure.story("Авторизация в админ-панели")
@allure.severity(allure.severity_level.CRITICAL)
def test_admin_login_logout(browser):
    """Тест авторизации и выхода из админ-панели"""
    with allure.step("Инициализация страницы администрирования"):
        ap = AdminPage()

    with allure.step("Открытие страницы админ-панели"):
        browser.open(ap.ADMIN_PAGE)

    with allure.step("Выполнение авторизации администратора"):
        ap.authorization_admin(browser)

    with allure.step("Выполнение выхода из системы"):
        ap.logout(browser)


@pytest.mark.frontend
@allure.feature("Корзина товаров")
@allure.story("Добавление товара в корзину")
def test_add_random_product_to_cart(browser):
    """Тест добавления товара в корзину"""
    with allure.step("Инициализация страницы каталога"):
        cp = CatalogPage()

    with allure.step("Переход на главную страницу"):
        cp.header.click_logo(browser=browser)

    with allure.step("Установка масштаба страницы для лучшей видимости"):
        cp.header.set_page_zoom(browser)

    with allure.step("Добавление случайного товара в корзину"):
        product_name = cp.add_product_cart(browser=browser)
        allure.dynamic.title(f"Добавление товара '{product_name}' в корзину")

    with allure.step("Проверка наличия товара в корзине"):
        cp.checking_product_cart(browser=browser, product_name=product_name)


@pytest.mark.frontend
@pytest.mark.parametrize("currency_action", [
    "change_to_eur",
    "change_to_gbp",
    "change_to_usd"
], ids=["EUR", "GBP", "USD"])
@allure.feature("Валюты")
@allure.story("Смена валюты на главной странице")
def test_select_currency_title(browser, currency_action):
    """Тест смены валюты на главной странице"""
    with allure.step("Инициализация страницы каталога"):
        cp = CatalogPage()

    with allure.step("Переход на главную страницу"):
        cp.header.click_logo(browser)

    with allure.step("Установка оптимального масштаба страницы"):
        cp.header.set_page_zoom(browser)

    with allure.step("Получение текущих цен товаров"):
        prices_before = cp.get_current_product_prices(browser)
        allure.attach(
            str(prices_before),
            name="Цены до смены валюты",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Смена валюты"):
        new_currency = cp.header.change_currency(browser)
        allure.attach(
            new_currency,
            name="Выбранная валюта",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Корректировка масштаба после изменений"):
        cp.header.set_page_zoom(browser)

    with allure.step("Верификация изменения цен"):
        cp.verify_currency_changed(original_prices=prices_before, new_prices=new_currency)


@pytest.mark.frontend
@allure.feature("Валюты")
@allure.story("Смена валюты в различных категориях каталога")
def test_select_currency_catalog(browser):
    """Тест смены валюты в Каталоге"""
    with allure.step("Инициализация страницы каталога"):
        cp = CatalogPage()

    with allure.step("Выбор категории товаров из каталога"):
        cp.select_random_menu_item_and_show_all(browser)

    with allure.step("Получение цен товаров в выбранной категории"):
        prices_before = cp.get_current_product_prices(browser)
        allure.attach(
            str(prices_before),
            name=f"Цены до смены валюты",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Смена валюты"):
        new_currency = cp.header.change_currency(browser)
        allure.attach(
            new_currency,
            name="Новая валюта",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Корректировка отображения страницы"):
        cp.header.set_page_zoom(browser)

    with allure.step("Проверка изменения цен в категории"):
        cp.verify_currency_changed(original_prices=prices_before, new_prices=new_currency)


@pytest.mark.frontend
@pytest.mark.parametrize("user_type", [
    ("Test", "User", "standard"),
    ("Admin", "Test", "admin"),
    ("John", "Doe", "customer")
], ids=["standard_user", "admin_user", "customer_user"])
@allure.feature("Управление пользователями")
@allure.story("Регистрация новых пользователей")
def test_opencart_add_user(browser, user_type):
    """Тест регистрации нового пользователя в магазине opencart"""
    firstname, lastname, user_role = user_type

    with allure.step("Инициализация страницы администрирования"):
        ap = AdminPage()

    with allure.step("Открытие админ-панели"):
        browser.open(ap.ADMIN_PAGE)

    with allure.step("Авторизация администратора"):
        ap.authorization_admin(browser)

    with allure.step(f"Добавление пользователя: {firstname} {lastname} ({user_role})"):
        value, email = ap.add_customers(browser)
        allure.dynamic.title(f"Добавление пользователя {firstname} {lastname}")

    with allure.step("Верификация данных пользователя"):
        ap.verifying_user_data(browser, firstname=value, lastname=value, email=email)


@pytest.mark.frontend
@allure.feature("Управление товарами")
@allure.story("Добавление и удаление товаров")
def test_opencart_add_and_delete_product(browser, product_category):
    """Тест по добавлению и удалению нового товара в разделе администратора"""

    with allure.step("Инициализация страницы администрирования"):
        ap = AdminPage()

    with allure.step("Открытие админ-панели"):
        browser.open(ap.ADMIN_PAGE)

    with allure.step("Авторизация администратора"):
        ap.authorization_admin(browser)

    with allure.step(f"Добавление товара"):
        value = ap.add_product(browser)
        allure.dynamic.title(f"Добавление товара '{value}'")

    with allure.step("Проверка данных товара"):
        ap.verifying_product_data(browser, value=value)

    with allure.step("Удаление товара"):
        ap.delete_product(browser)
