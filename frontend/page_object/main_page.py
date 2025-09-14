import random

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

    @allure.step("Добавление случайного товара в список")
    def add_product_to_list(self, browser, list_type="cart"):
        """
        Универсальный метод добавления товара в список (cart или wishlist)

        :param browser: экземпляр браузера
        :param list_type: тип списка - "cart" или "wishlist"
        :return: название добавленного товара
        """
        self.logger.info(f"Начало добавления случайного товара в {list_type}")

        button_locator = self.BUTTON_ADD_TO_CART if list_type == "cart" else self.BUTTON_ADD_TO_WISH_LIST
        list_name = "корзину" if list_type == "cart" else "список желаний"

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
                    raise Exception(f"Не найдено подходящих товаров для добавления в {list_name}")

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

            with allure.step(f"3. Нажать кнопку 'Добавить в {list_name}'"):
                self.logger.info(f"Нажатие кнопки 'Добавить в {list_name}'")
                self.wait_and_click(browser=random_product, target_locator=button_locator, method=By.CSS_SELECTOR)

            with allure.step("4. Проверить уведомление об успешном добавлении"):
                self.logger.info("Проверка уведомления об успешном добавлении")
                self.wait_element(browser=random_product, target_locator=self.header.ALERT_SUCCESS)

                if list_type == "wishlist":
                    self.wait_and_click(browser=browser, target_locator=self.header.BUTTON_CLOSE_ALERT)

            self.logger.info(f"Товар '{product_name}' успешно добавлен в {list_name}")
            return product_name

    @allure.step("Проверка наличия товара в списке")
    def checking_product_in_list(self, browser, product_name, list_type="cart"):
        """
        Универсальный метод проверки товара в списке (cart или wishlist)

        :param browser: экземпляр браузера
        :param product_name: название товара для проверки
        :param list_type: тип списка - "cart" или "wishlist"
        """
        list_name = "корзину" if list_type == "cart" else "список желаний"
        self.logger.info(f"Проверка наличия товара '{product_name}' в {list_name}")

        items_locator = self.header.CART_ITEMS_LIST if list_type == "cart" else self.header.WISH_LIST_ITEM
        success_action = self.header.CART if list_type == "cart" else self.header.BUTTON_WISH_LIST

        with allure.step(f"1. Перейти в {list_name}"):
            self.logger.info(f"Переход в {list_name}")
            self.wait_and_click(browser=browser, target_locator=success_action)

        with allure.step(f"2. Проверить что {list_name} не пуст(-а) (ожидаемый товар: '{product_name}')"):
            self.logger.info(f"Проверка что {list_name} не пуст(-а)")
            items_in_list = self.wait_elements(browser, target_locator=items_locator)
            self.logger.info(f"Количество товаров в списке: {len(items_in_list)}")
            allure.attach(
                str(len(items_in_list)),
                name=f"Количество товаров в списке",
                attachment_type=allure.attachment_type.TEXT
            )
            assert len(items_in_list) > 0, f"В {list_name.capitalize()} нет товаров"

        with allure.step("3. Поиск товара в списке"):
            self.logger.info(f"Поиск товара '{product_name}' в {list_name}")
            found = False
            for item in items_in_list:
                if product_name in item.text:
                    found = True
                    self.logger.info(f"Товар найден: {item.text}")
                    allure.attach(
                        item.text,
                        name="Найденный товар",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    break

        with allure.step(f"4. Проверить что товар '{product_name}' присутствует в {list_name}"):
            self.logger.info(f"Проверка наличия товара в {list_name}")
            assert found, f"Товар '{product_name}' не найден в {list_name}"
            self.logger.info(f"Товар '{product_name}' успешно найден в {list_name}")


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