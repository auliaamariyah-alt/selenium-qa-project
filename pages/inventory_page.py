# pages/inventory_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class InventoryPage(BasePage):
    URL = 'https://www.saucedemo.com/inventory.html'

    SORT_DROPDOWN   = (By.CLASS_NAME, 'product_sort_container')
    PRODUCT_NAMES   = (By.CLASS_NAME, 'inventory_item_name')
    PRODUCT_PRICES  = (By.CLASS_NAME, 'inventory_item_price')
    ADD_TO_CART_BTNS = (By.CSS_SELECTOR, '[data-test^=add-to-cart]')
    REMOVE_BTNS     = (By.CSS_SELECTOR, '[data-test^=remove]')
    CART_BADGE      = (By.CLASS_NAME, 'shopping_cart_badge')
    CART_ICON       = (By.CLASS_NAME, 'shopping_cart_link')
    BURGER_MENU     = (By.ID, 'react-burger-menu-btn')
    LOGOUT_LINK     = (By.ID, 'logout_sidebar_link')

    def get_product_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_NAMES))

    def sort_by(self, option):
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(option)

    def get_all_prices(self):
        els = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [float(e.text.replace('$', '')) for e in els]

    def add_product_to_cart(self, index=0):
        btns = self.driver.find_elements(*self.ADD_TO_CART_BTNS)
        btns[index].click()

    def remove_product_from_cart(self, index=0):
        btns = self.driver.find_elements(*self.REMOVE_BTNS)
        btns[index].click()

    def get_cart_count(self):
        try:
            return int(self.get_text(self.CART_BADGE))
        except:
            return 0

    def go_to_cart(self):
        self.click(self.CART_ICON)

    def logout(self):
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)