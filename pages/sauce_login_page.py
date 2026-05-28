# pages/sauce_login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SauceDemoLoginPage(BasePage):
    URL = 'https://www.saucedemo.com'

    USERNAME  = (By.ID, 'user-name')
    PASSWORD  = (By.ID, 'password')
    LOGIN_BTN = (By.ID, 'login-button')
    ERROR_MSG = (By.CSS_SELECTOR, '[data-test=error]')

    def navigate(self):
        self.open(self.URL)

    def login(self, username, password):
        self.navigate()
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)

    def is_login_failed(self):
        return self.is_visible(self.ERROR_MSG)