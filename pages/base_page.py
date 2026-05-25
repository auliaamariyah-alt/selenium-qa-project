# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging

class BasePage:
    TIMEOUT = 10
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)
        self.logger = logging.getLogger(self.__class__.__name__)
 # ── Navigasi ──────────────────────────────────────
    def open(self, url):
        self.logger.info(f'Membuka URL: {url}')
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url
 # ── Elemen ────────────────────────────────────────
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.logger.info(f'Klik elemen: {locator}')
        self.find_clickable(locator).click()

    def type(self, locator, text):
        self.logger.info(f'Ketik "{text}" pada: {locator}')
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except:
            return False

    def take_screenshot(self, name):
        self.driver.save_screenshot(f'reports/screenshots/{name}.png')