import allure

from frontend.page_object.base_test import BasePage
from frontend.page_object.header_elements import HeaderElements


class AccountLoginPage(BasePage):
    """Элементы, которые есть на всех страницах"""

    INPUT_EMAIL = "//input[contains(@name, 'email')]"
    INPUT_PASSWORD = "//input[contains(@name, 'password')]"
    BUTTON_LOGIN = "//button[contains(text(), 'Login')]"

    def __init__(self):
        super().__init__()
        self.header = HeaderElements()

    @allure.step("Авторизация пользователя")
    def account_login(self, browser, email, password):
        self.wait_and_click(browser=browser, target_locator=self.header.MY_ACCOUNT_DROPDOWN)
        self.wait_and_click(browser=browser, target_locator=self.header.LOGIN_LINK)
        self.wait_element(browser=browser, target_locator=self.INPUT_EMAIL)
        self.data_entry(browser=browser, target=self.INPUT_EMAIL, value=email)
        self.data_entry(browser=browser, target=self.INPUT_PASSWORD, value=password)
        self.wait_and_click(browser=browser, target_locator=self.BUTTON_LOGIN)
