import random
import time

import allure
from frontend.page_object.base_test import BasePage
from selenium.webdriver.common.by import By

from frontend.page_object.header_elements import HeaderElements


class MainPage(BasePage):
    """Главная страница OpenCart"""
    CAROUSEL_BANNER = "#carousel-banner-0"
    ALL_PRODUCT_NAME = ".product-thumb"
    TITLE_PRODUCT_NAME = "h4 a"
    BUTTON_ADD_TO_CART = "button[formaction*='cart.add']"
    BUTTON_ADD_TO_WISH_LIST = "button[formaction*='wishlist.add']"
    FIRST_PRODUCT = ".product-thumb:first-child"

    def __init__(self):
        super().__init__()
        self.header = HeaderElements()

    @allure.step("Добавление случайного товара в корзину")
    def add_product_cart(self, browser):
        """Добавление случайного товара в корзину с проверкой успешности операции"""
        self.logger.info("Начало добавления случайного товара в корзину")

        with allure.step("1. Получить список всех товаров на странице"):
            self.logger.info("Получение списка всех товаров")
            all_products = self.wait_elements(browser, target_locator=self.ALL_PRODUCT_NAME,method=By.CSS_SELECTOR)

            self.logger.info(f"Найдено товаров: {len(all_products)}")
            allure.attach(
                str(len(all_products)),
                name="Количество найденных товаров",
                attachment_type=allure.attachment_type.TEXT
            )

            with allure.step("2. Выбрать случайный товар"):
                filtered_products = []
                for product in all_products:
                    product_name = product.find_element(By.CSS_SELECTOR, self.TITLE_PRODUCT_NAME).text
                    if product_name not in ['Apple Cinema 30"', 'Canon EOS 5D']:
                        filtered_products.append(product)

                if not filtered_products:
                    raise Exception("Не найдено подходящих товаров для добавления в корзину")

                self.logger.info(f"Доступно товаров после фильтрации: {len(filtered_products)}")
                allure.attach(
                    str(len(filtered_products)),
                    name="Количество товаров после фильтрации",
                    attachment_type=allure.attachment_type.TEXT
                )
                random_product = random.choice(filtered_products)
                product_name = random_product.find_element(By.CSS_SELECTOR, self.TITLE_PRODUCT_NAME).text
                self.logger.info(f"Выбран товар: {product_name}")
                allure.attach(
                    product_name,
                    name="Название выбранного товара",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("3. Нажать кнопку 'Добавить в корзину'"):
                self.logger.info("Нажатие кнопки 'Добавить в корзину'")
                self.wait_and_click(browser=random_product, target_locator=self.BUTTON_ADD_TO_CART, method=By.CSS_SELECTOR)

            with allure.step("4. Проверить уведомление об успешном добавлении"):
                self.logger.info("Проверка уведомления об успешном добавлении")
                self.wait_element(browser=random_product, target_locator=self.header.ALERT_SUCCESS)

            with allure.step("5. Перейти в корзину"):
                self.logger.info("Переход в корзину")
                self.wait_and_click(browser=browser, target_locator=self.header.CART, method=By.CSS_SELECTOR)

        self.logger.info(f"Товар '{product_name}' успешно добавлен в корзину")
        return product_name

    @allure.step("Добавление случайного товара в список желаний")
    def add_product_wish_list(self, browser):
        """Добавление случайного товара в список желаний с проверкой успешности операции"""
        self.logger.info("Начало добавления случайного товара в список желаний")

        with allure.step("1. Получить список всех товаров на странице"):
            self.logger.info("Получение списка всех товаров")
            all_products = self.wait_elements(browser, target_locator=self.ALL_PRODUCT_NAME, method=By.CSS_SELECTOR)

            self.logger.info(f"Найдено товаров: {len(all_products)}")
            allure.attach(
                str(len(all_products)),
                name="Количество найденных товаров",
                attachment_type=allure.attachment_type.TEXT
            )

            with allure.step("2. Выбрать случайный товар"):
                filtered_products = []
                for product in all_products:
                    product_name = product.find_element(By.CSS_SELECTOR, self.TITLE_PRODUCT_NAME).text
                    if product_name not in ['Apple Cinema 30"', 'Canon EOS 5D']:
                        filtered_products.append(product)

                if not filtered_products:
                    raise Exception("Не найдено подходящих товаров для добавления в список желаний")

                self.logger.info(f"Доступно товаров после фильтрации: {len(filtered_products)}")
                allure.attach(
                    str(len(filtered_products)),
                    name="Количество товаров после фильтрации",
                    attachment_type=allure.attachment_type.TEXT
                )
                random_product = random.choice(filtered_products)
                product_name = random_product.find_element(By.CSS_SELECTOR, self.TITLE_PRODUCT_NAME).text
                self.logger.info(f"Выбран товар: {product_name}")
                allure.attach(
                    product_name,
                    name="Название выбранного товара",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("3. Нажать кнопку 'Добавить в список желаний'"):
                self.logger.info("Нажатие кнопки 'Добавить в список желаний'")
                self.wait_and_click(browser=random_product, target_locator=self.BUTTON_ADD_TO_WISH_LIST,
                                    method=By.CSS_SELECTOR)

            with allure.step("4. Проверить уведомление об успешном добавлении"):
                self.logger.info("Проверка уведомления об успешном добавлении")
                self.wait_element(browser=random_product, target_locator=self.header.ALERT_SUCCESS)
            with allure.step("5. Перейти в список желаний"):
                self.logger.info("Переход в список желаний")
                self.wait_and_click(browser=browser, target_locator=self.header.BUTTON_WISH_LIST)
        self.logger.info(f"Товар '{product_name}' успешно добавлен в список желаний")
        return product_name

    @allure.step("Проверка наличия товара в корзине")
    def checking_product_cart(self, browser, product_name):
        """Проверка, что указанный товар присутствует в корзине"""
        self.logger.info(f"Проверка наличия товара '{product_name}' в корзине")

        with allure.step(f"1. Проверить что корзина не пуста (ожидаемый товар: '{product_name}')"):
            self.logger.info("Проверка что корзина не пуста")
            items_in_cart = self.wait_elements(browser, target_locator=self.header.CART_ITEMS_LIST,method=By.CSS_SELECTOR)
            self.logger.info(f"Количество товаров в корзине: {len(items_in_cart)}")
            allure.attach(
                str(len(items_in_cart)),
                name="Количество товаров в корзине",
                attachment_type=allure.attachment_type.TEXT
            )
            assert len(items_in_cart) > 0, "Корзина пуста"

        with allure.step("2. Поиск товара в корзине"):
            self.logger.info(f"Поиск товара '{product_name}' в корзине")
            found = False
            for item in items_in_cart:
                if product_name in item.text:
                    found = True
                    self.logger.info(f"Товар найден: {item.text}")
                    allure.attach(
                        item.text,
                        name="Найденный товар",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    break

        with allure.step(f"3. Проверить что товар '{product_name}' присутствует в корзине"):
            self.logger.info("Проверка наличия товара в корзине")
            assert found, f"Товар '{product_name}' не найден в корзине"
            self.logger.info(f"Товар '{product_name}' успешно найден в корзине")

    @allure.step("Проверка наличия товара в корзине")
    def checking_product_wish_list(self, browser, product_name):
        """Проверка, что указанный товар присутствует в корзине"""
        self.logger.info(f"Проверка наличия товара '{product_name}' в корзине")

        with allure.step(f"1. Проверить что корзина не пуста (ожидаемый товар: '{product_name}')"):
            self.logger.info("Проверка что корзина не пуста")
            items_in_cart = self.wait_elements(browser, target_locator=self.header.WISH_LIST_ITEM)
            self.logger.info(f"Количество товаров в корзине: {len(items_in_cart)}")
            allure.attach(
                str(len(items_in_cart)),
                name="Количество товаров в корзине",
                attachment_type=allure.attachment_type.TEXT
            )
            assert len(items_in_cart) > 0, "Корзина пуста"

        with allure.step("2. Поиск товара в корзине"):
            self.logger.info(f"Поиск товара '{product_name}' в корзине")
            found = False
            for item in items_in_cart:
                if product_name in item.text:
                    found = True
                    self.logger.info(f"Товар найден: {item.text}")
                    allure.attach(
                        item.text,
                        name="Найденный товар",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    break

        with allure.step(f"3. Проверить что товар '{product_name}' присутствует в корзине"):
            self.logger.info("Проверка наличия товара в корзине")
            assert found, f"Товар '{product_name}' не найден в корзине"
            self.logger.info(f"Товар '{product_name}' успешно найден в корзине")

    @allure.step("Проверка элементов на главной странице")
    def check_elements_main_page(self, browser):
        """Проверка элементов на главной странице"""
        self.logger.info("Проверка элементов на главной странице")

        with allure.step("Проверить наличие логотипа"):
            self.logger.info("Проверка логотипа")
            self.wait_element(browser, target_locator=self.header.LOGO)

        with allure.step("Проверить поле поиска"):
            self.logger.info("Проверка поля поиска")
            self.wait_element(browser, target_locator=self.header.SEARCH_INPUT, method=By.CSS_SELECTOR)

        with allure.step("Проверить корзину"):
            self.logger.info("Проверка корзины")
            self.wait_element(browser, target_locator=self.header.CART, method=By.CSS_SELECTOR)

        with allure.step("Проверить карусель баннеров"):
            self.logger.info("Проверка карусели баннеров")
            self.wait_element(browser, target_locator=self.CAROUSEL_BANNER, method=By.CSS_SELECTOR)

        with allure.step("Проверить навигационное меню"):
            self.logger.info("Проверка навигационного меню")
            self.wait_element(browser, target_locator=self.header.NARBAR_MENU)

        self.logger.info("Все элементы на главной странице присутствуют")