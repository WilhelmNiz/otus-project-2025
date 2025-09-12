import allure
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from frontend.page_object.main_page import MainPage


class CatalogPage(MainPage):
    """Страница каталога товаров"""

    # Путь до цен товаров
    PRICE = "div.price"

    # Путь до списка товаров
    PRODUCT_LIST = "#product-list"

    # Путь до наименований товаров
    PRODUCT_NAME = ".product-thumb h4 a"

    @allure.step("Выбрать случайный пункт меню и нажать 'Показать все'")
    def select_random_menu_item_and_show_all(self, browser):
        """
        Выбирает случайный пункт меню и нажимает "Показать все" в выбранной категории.
        """
        self.logger.info("Начало выбора случайного пункта меню")

        with allure.step("1. Получить все пункты выпадающего меню"):
            self.logger.info("Получение пунктов выпадающего меню")
            menu_items = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, self.header.NARBAR_MENU_DROPDOWN)))
            self.logger.info(f"Найдено пунктов меню: {len(menu_items)}")
            allure.attach(
                str([item.text for item in menu_items]),
                name="Available menu items",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step(f"2. Выбрать случайный пункт меню (всего {len(menu_items)} вариантов)"):
            select_product = random.choice(menu_items)
            selected_text = select_product.text
            self.logger.info(f"Выбран пункт меню: {selected_text}")
            allure.attach(
                selected_text,
                name="Selected menu item",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step(f"3. Кликнуть на выбранный пункт: '{selected_text}'"):
            self.logger.info(f"Клик по выбранному пункту: {selected_text}")
            select_product.click()

        with allure.step("4. Нажать 'Показать все' в выбранной категории"):
            self.logger.info("Нажатие 'Показать все' в выбранной категории")
            self.wait_and_click(browser=browser, target_locator=self.header.PRODUCT_SHOW_ALL)

        self.logger.info("Случайный пункт меню успешно выбран")

    @allure.step("Получение текущих цен товаров")
    def get_current_product_prices(self, browser, count=3):
        """
        Получает текущие цены товаров на странице.
        """
        self.logger.info(f"Получение первых {count} цен товаров")

        with allure.step(f"1. Получить первые {count} цен товаров"):
            product_prices = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.PRICE)))

            prices_list = [price.text for price in product_prices[:count]]
            self.logger.info(f"Получены цены: {prices_list}")

            allure.attach(
                "\n".join(prices_list),
                name=f"Первые {count} цен товаров",
                attachment_type=allure.attachment_type.TEXT
            )

            return prices_list

    @allure.step("Проверка изменения цен после смены валюты")
    def verify_currency_changed(self, original_prices, new_prices):
        """
        Проверяет, что цены изменились после смены валюты.
        """
        self.logger.info("Проверка изменения цен после смены валюты")
        self.logger.info(f"Исходные цены: {original_prices}")
        self.logger.info(f"Новые цены: {new_prices}")

        assert original_prices != new_prices, "Цены товаров не изменились после смены валюты"
        self.logger.info("Цены успешно изменились после смены валюты")

    @allure.step("Проверка элементов на странице каталога")
    def check_elements_catalog_page(self, browser):
        """Проверка наличия основных элементов на странице каталога"""
        self.logger.info("Проверка элементов на странице каталога")

        with allure.step("1. Проверить наличие списка товаров"):
            self.logger.info("Проверка списка товаров")
            self.wait_element(browser, target_locator=self.PRODUCT_LIST, method=By.CSS_SELECTOR)

        with allure.step("2. Проверить кнопку поиска"):
            self.logger.info("Проверка кнопки поиска")
            self.wait_element(browser, target_locator=self.header.SEARCH_BUTTON, method=By.CSS_SELECTOR)

        with allure.step("3. Проверить поле ввода поиска"):
            self.logger.info("Проверка поля ввода поиска")
            self.wait_element(browser, target_locator=self.header.SEARCH_INPUT, method=By.CSS_SELECTOR)

        with allure.step("4. Проверить наличие логотипа"):
            self.logger.info("Проверка логотипа")
            self.wait_element(browser, target_locator=self.header.LOGO)

        with allure.step("5. Проверить названия товаров"):
            self.logger.info("Проверка названий товаров")
            self.wait_element(browser, target_locator=self.PRODUCT_NAME, method=By.CSS_SELECTOR)

        self.logger.info("Все элементы на странице каталога присутствуют")