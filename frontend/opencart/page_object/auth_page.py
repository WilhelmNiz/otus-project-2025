from selenium.webdriver.common.by import By

from frontend.opencart.page_object.main_page import MainPage


class AuthPage(MainPage):
    """Страницы входа и регистрации"""
    FIRSTNAME_INPUT = "#input-firstname"
    LASTNAME_INPUT = "#input-lastname"
    EMAIL_INPUT = "#input-email"
    REGISTER_FORM = "#form-register > div > button"
    INPUT_PASSWORD = "#input-password"
    INPUT_USERNAME = "#input-username"
    BUTTON_LOGIN = "#form-login > div.text-end > button"
    CARD_HEADER = "#content > div > div > div > div > div.card-header"
    BUTTON_LOGOUT = "#nav-logout > a"

    def check_elements_auth_page(self, browser):
        """Проверка элементов на странице авторизации"""
        self.logger.info("Проверка элементов на странице авторизации")

        self.logger.info("Проверка наличия логотипа")
        self.wait_element(browser, target_locator=self.header.LOGO)

        self.logger.info("Проверка поля ввода имени")
        self.wait_element(browser, target_locator=self.FIRSTNAME_INPUT, method=By.CSS_SELECTOR)

        self.logger.info("Проверка поля ввода фамилии")
        self.wait_element(browser, target_locator=self.LASTNAME_INPUT, method=By.CSS_SELECTOR)

        self.logger.info("Проверка поля ввода email")
        self.wait_element(browser, target_locator=self.EMAIL_INPUT, method=By.CSS_SELECTOR)

        self.logger.info("Проверка формы регистрации")
        self.wait_element(browser, target_locator=self.REGISTER_FORM, method=By.CSS_SELECTOR)

        self.logger.info("Все элементы на странице авторизации присутствуют")

    def open_auth_page(self, browser):
        """Открытие страницы регистрации"""
        self.logger.info("Открытие страницы регистрации")

        self.logger.info("Клик по выпадающему меню 'Мой аккаунт'")
        self.wait_and_click(
            browser=browser,
            target_locator=self.header.MY_ACCOUNT_DROPDOWN,
            method=By.CSS_SELECTOR
        )

        self.logger.info("Клик по ссылке 'Регистрация'")
        self.wait_and_click(
            browser=browser,
            target_locator=self.header.REGISTER_LINK,
            method=By.CSS_SELECTOR
        )

        self.logger.info("Страница регистрации успешно открыта")