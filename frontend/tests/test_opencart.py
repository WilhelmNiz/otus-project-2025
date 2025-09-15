import allure
import pytest
from frontend.page_object.catalog_page import CatalogPage
from frontend.page_object.admin_page import AdminPage
from frontend.page_object.account_login_page import AccountLoginPage
from frontend.page_object.listpage import ListPage
from frontend.page_object.main_page import MainPage


@pytest.mark.frontend
@allure.feature("Администрирование OpenCart")
@allure.story("Авторизация в админ-панели")
@allure.title("Тест авторизации и выхода из админ-панели")
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
@allure.feature("Управление товарами")
@allure.story("Добавление товара в корзину")
def test_add_random_product_to_cart(browser):
    """Тест добавления товара в корзину"""
    with allure.step("Инициализация страницы каталога"):
        cp = CatalogPage()
        lp = ListPage()
        mp = MainPage()

    with allure.step("Переход на главную страницу"):
        cp.header.click_logo(browser)
        cp.header.set_page_zoom(browser)

    with allure.step("Добавление случайного товара в корзину"):
        product_name = mp.add_product_to_list(browser, list_type="cart")
        allure.dynamic.title(f"Добавление товара '{product_name}' в корзину")

    with allure.step("Проверка наличия товара в корзине"):
        lp.checking_product_in_list(browser, product_name=product_name, list_type="cart")


@pytest.mark.frontend
@allure.feature("Валюты")
@allure.story("Смена валюты на главной странице")
def test_select_currency_title(browser):
    """Тест смены валюты на главной странице"""
    with allure.step("Инициализация страницы каталога"):
        cp = CatalogPage()

    with allure.step("Переход на главную страницу"):
        cp.header.click_logo(browser)
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
        new_currency = str(new_currency)
        allure.attach(
            new_currency,
            name="Выбранная валюта",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.dynamic.title(f"Смена валюты на главной странице {new_currency}")

    with allure.step("Корректировка масштаба после изменений"):
        cp.header.set_page_zoom(browser)

    with allure.step("Получение новых цен после смены валюты"):
        prices_after = cp.get_current_product_prices(browser)
        allure.attach(
            str(prices_after),
            name=f"Цены помле смены валюты",
            attachment_type=allure.attachment_type.TEXT
        )
    with allure.step("Верификация изменения цен"):
        cp.verify_currency_changed(original_prices=prices_before, new_prices=prices_after,
                                   currency_name=new_currency)


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
        new_currency = str(new_currency)
        allure.attach(
            new_currency,
            name="Выбранная валюта",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.dynamic.title(f"Смена валюты в каталоге {new_currency}")

    with allure.step("Корректировка отображения страницы"):
        cp.header.set_page_zoom(browser)

    with allure.step("Получение новых цен после смены валюты"):
        prices_after = cp.get_current_product_prices(browser)
        allure.attach(
            str(prices_after),
            name=f"Цены помле смены валюты",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Проверка изменения цен в категории"):
        cp.verify_currency_changed(original_prices=prices_before, new_prices=prices_after,
                                   currency_name=new_currency)


@pytest.mark.frontend
@pytest.mark.parametrize("user_data", [
    {"firstname": "Test", "lastname": "User", "password": "test123"},
    {"firstname": "Admin", "lastname": "Test", "password": "admin123"},
    {"firstname": "John", "lastname": "Doe", "password": "customer1"},
    {"firstname": "Alice", "lastname": "Smith", "password": "alice123"},
    {"firstname": "Bob", "lastname": "Johnson", "password": "bob123!"}
])
@allure.feature("Администрирование OpenCart")
@allure.story("Регистрация новых пользователей через админ панель")
def test_opencart_add_and_delete_user(browser, user_data):
    """Тест регистрации и удаления нового пользователя в админ панели"""
    firstname = user_data["firstname"]
    lastname = user_data["lastname"]
    password = user_data["password"]

    with allure.step("Инициализация страницы администрирования"):
        ap = AdminPage()

    with allure.step("Открытие админ-панели"):
        browser.open(ap.ADMIN_PAGE)

    with allure.step("Авторизация администратора"):
        ap.authorization_admin(browser)

    with allure.step(f"Добавление пользователя: {firstname} {lastname}"):
        added_firstname, added_lastname, email = ap.add_customers(
            browser,
            firstname=firstname,
            lastname=lastname,
            password=password
        )
        allure.dynamic.title(f"Добавление пользователя {firstname} {lastname}")

        allure.attach(
            f"Имя: {added_firstname}\nФамилия: {added_lastname}\nEmail: {email}",
            name="Данные добавленного пользователя",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Верификация данных пользователя в системе"):
        ap.verifying_user_data(browser, firstname=added_firstname, lastname=added_lastname, email=email)

    with allure.step("Удаление созданного пользователя"):
        ap.delete_entity(browser, entity_type="Пользователь")

@pytest.mark.frontend
@allure.feature("Управление товарами")
@allure.story("Добавление и удаление товаров")
def test_opencart_add_and_delete_product(browser):
    """Тест по добавлению и удалению нового товара в разделе администратора"""

    with allure.step("Инициализация страницы администрирования"):
        ap = AdminPage()

    with allure.step("Открытие админ-панели"):
        browser.open(ap.ADMIN_PAGE)

    with allure.step("Авторизация администратора"):
        ap.authorization_admin(browser)

    with allure.step("Добавление товара"):
        value = ap.add_product(browser)
        allure.dynamic.title(f"Добавление товара '{value}'")

    with allure.step("Проверка данных товара"):
        ap.verifying_product_data(browser, value=value)

    with allure.step("Удаление товара"):
        ap.delete_entity(browser)


@pytest.mark.frontend
@allure.feature("Управление товарами")
@allure.story("Добавление товара в список желаний")
def test_add_random_product_to_wish_list(browser):
    """Тест добавления в список желаний"""
    password = 4444

    with allure.step("Инициализация страниц"):
        ap = AdminPage()
        cp = CatalogPage()
        al = AccountLoginPage()
        lp = ListPage()
        mp = MainPage()

    with allure.step("Открытие админ-панели"):
        browser.open(ap.ADMIN_PAGE)

    with allure.step("Авторизация администратора"):
        ap.authorization_admin(browser)

    with allure.step("Добавление пользователя"):
        added_firstname, added_lastname, email = ap.add_customers(
            browser,
            firstname="Test123",
            lastname="Test123",
            password=password
        )

        allure.attach(
            f"Имя: {added_firstname}\nФамилия: {added_lastname}\nEmail: {email}",
            name="Данные добавленного пользователя",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Открытие главной страницы"):
        browser.go_to_home()

    with allure.step("Переход на главную страницу"):
        cp.header.click_logo(browser)
        cp.header.set_page_zoom(browser)

    with allure.step("Авторизация пользователя на сайте"):
        al.account_login(browser, email=email, password=password)

    with allure.step("Переход на главную страницу"):
        cp.header.click_logo(browser)
        cp.header.set_page_zoom(browser)

    with allure.step("Добавление случайного товара в список желаний"):
        product_name = mp.add_product_to_list(browser, list_type="wishlist")
        allure.dynamic.title(f"Добавление товара '{product_name}' в список желаний")

    with allure.step("Проверка наличия товара в список желаний"):
        lp.checking_product_in_list(browser, product_name=product_name, list_type="wishlist")