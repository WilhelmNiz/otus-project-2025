import random

import allure
from selenium.webdriver.common.by import By

from frontend.page_object.base_page_with_header import BasePageWithHeader


class MainPage(BasePageWithHeader):
    """Главная страница OpenCart"""
    CAROUSEL_BANNER = "#carousel-banner-0"
    ALL_PRODUCT_NAME = ".product-thumb"
    TITLE_PRODUCT_NAME = "h4 a"
    BUTTON_ADD_TO_CART = "button[formaction*='cart.add']"
    BUTTON_ADD_TO_WISH_LIST = "button[formaction*='wishlist.add']"

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
                self.wait_and_click(browser=browser, target_locator=self.header.BUTTON_CLOSE_ALERT)

            self.logger.info(f"Товар '{product_name}' успешно добавлен в {list_name}")
            return product_name