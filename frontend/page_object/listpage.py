import allure

from frontend.page_object.base_page_with_header import BasePageWithHeader


class ListPage(BasePageWithHeader):
    """Универсальная страница для работы с списками (cart и wishlist)"""
    CART_ITEMS_LIST = "//h1[contains(text(), 'Shopping Cart')]/following::table//tbody/tr"
    WISH_LIST_ITEM = "//h1[contains(text(), 'My Wishlist')]/following::table//tbody/tr"

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

        items_locator = self.CART_ITEMS_LIST if list_type == "cart" else self.WISH_LIST_ITEM
        success_action = self.header.BUTTON_CART if list_type == "cart" else self.header.BUTTON_WISH_LIST

        with allure.step(f"1. Перейти в {list_name}"):
            self.logger.info(f"Переход в {list_name}")
            self.wait_and_click(browser=browser, target_locator=success_action)

        with allure.step(f"2. Проверить что список не пуст (ожидаемый товар: '{product_name}')"):
            self.logger.info(f"Проверка что список не пуст")
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