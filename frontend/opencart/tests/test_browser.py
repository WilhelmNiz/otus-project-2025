from frontend.opencart.page_object.main_page import MainPage
from frontend.opencart.page_object.catalog_page import CatalogPage
from frontend.opencart.page_object.admin_page import AdminPage
from frontend.opencart.page_object.auth_page import AuthPage
from frontend.opencart.page_object.product_page import ProductPage


def test_opencart_check_title(browser):
    """Тест проверки основных элементов главной страницы"""
    mp = MainPage()

    mp.check_elements_main_page(browser)


def test_opencart_catalog(browser):
    """Тест проверки элементов каталога товаров"""
    cp = CatalogPage()

    cp.header.click_logo(browser)
    cp.select_random_menu_item_and_show_all(browser)
    cp.check_elements_catalog_page(browser)


def test_opencart_product(browser):
    """Тест проверки элементов страницы товара"""
    pp = ProductPage()

    pp.open_product_page(browser)
    pp.check_elements_product_page(browser)


def test_opencart_check_admin(browser):
    """Тест проверки элементов страницы администрирования"""
    ap = AdminPage()

    browser.open(ap.ADMIN_PAGE)
    ap.check_elements_admin_page(browser)


def test_opencart_register(browser):
    """Тест проверки элементов страницы регистрации"""
    ap = AuthPage()

    ap.open_auth_page(browser)
    ap.check_elements_auth_page(browser)


def test_admin_login_logout(browser):
    """Тест авторизации и выхода из админ-панели"""

    ap = AdminPage()

    browser.open(ap.ADMIN_PAGE)
    ap.authorization_admin(browser)
    ap.logout(browser)


def test_add_random_product_to_cart(browser):
    """Тест добавления товара в корзину"""
    cp = CatalogPage()

    cp.header.click_logo(browser=browser)
    cp.header.set_page_zoom(browser)
    product_name = cp.add_product_cart(browser=browser)
    cp.checking_product_cart(browser=browser, product_name=product_name)


def test_select_currency_title(browser):
    """Тест смены валюты на главной странице"""

    cp = CatalogPage()

    cp.header.click_logo(browser)
    cp.header.set_page_zoom(browser)
    prices_before = cp.get_current_product_prices(browser)
    new_currency = cp.header.change_currency(browser)
    cp.header.set_page_zoom(browser)
    cp.verify_currency_changed(original_prices=prices_before, new_prices=new_currency)


def test_select_currency_catalog(browser):
    """Тест смены валюты в Каталоге"""
    cp = CatalogPage()

    cp.select_random_menu_item_and_show_all(browser)
    prices_before = cp.get_current_product_prices(browser)
    new_currency = cp.header.change_currency(browser)
    cp.header.set_page_zoom(browser)
    cp.verify_currency_changed(original_prices=prices_before, new_prices=new_currency)


def test_opencart_add_user(browser):
    """Тест регистрации нового пользователя в магазине opencart"""
    ap = AdminPage()

    browser.open(ap.ADMIN_PAGE)
    ap.authorization_admin(browser)
    value, email = ap.add_customers(browser)
    ap.verifying_user_data(browser, firstname=value, lastname=value, email=email)


def test_opencart_add_and_delete_product(browser):
    """Тест по добавлению и удалению нового товара в разделе администратора"""
    ap = AdminPage()

    browser.open(ap.ADMIN_PAGE)
    ap.authorization_admin(browser)
    value = ap.add_product(browser)
    ap.verifying_product_data(browser, value=value)
    ap.delete_product(browser)
