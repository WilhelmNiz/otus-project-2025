import allure
from selenium.webdriver.common.by import By

from page_object.main_page import MainPage


class ProductPage(MainPage):
    """Страница конкретного товара"""
    PRODUCT_TITLE = "h1"
    ADD_TO_CART_BTN = "#button-cart"

    @allure.step("Проверка элементов на странице товара")
    def check_elements_product_page(self, browser):
        """Проверка наличия основных элементов на странице товара"""
        self.logger.info("Начало проверки элементов на странице товара")

        with allure.step("1. Проверить логотип сайта"):
            self.logger.info("Проверка логотипа сайта")
            self.wait_element(browser, target_locator=self.header.LOGO)

        with allure.step("2. Проверить кнопку поиска"):
            self.logger.info("Проверка кнопки поиска")
            self.wait_element(browser, target_locator=self.header.SEARCH_BUTTON, method=By.CSS_SELECTOR)

        with allure.step("3. Проверить поле ввода поиска"):
            self.logger.info("Проверка поля ввода поиска")
            self.wait_element(browser, target_locator=self.header.SEARCH_INPUT, method=By.CSS_SELECTOR)

        with allure.step("4. Проверить контентную область страницы"):
            self.logger.info("Проверка контентной области страницы")
            self.wait_element(browser, target_locator=self.header.CONTENT, method=By.CSS_SELECTOR)

        with allure.step("5. Проверить кнопку 'Добавить в корзину'"):
            self.logger.info("Проверка кнопки 'Добавить в корзину'")
            self.wait_element(browser, target_locator=self.ADD_TO_CART_BTN, method=By.CSS_SELECTOR)

        self.logger.info("Все элементы на странице товара присутствуют")

    @allure.step("Открытие страницы товара")
    def open_product_page(self, browser):
        """Открытие страницы товара"""
        self.logger.info("Открытие страницы товара")

        self.logger.info("Клик по первому товару в списке")
        self.wait_and_click(browser=browser, target_locator=self.FIRST_PRODUCT, method=By.CSS_SELECTOR)

        self.logger.info("Страница товара успешно открыта")