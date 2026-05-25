# pages/login_page.py 
from selenium.webdriver.common.by import By 
from pages.base_page import BasePage 
  
class LoginPage(BasePage): 
    URL = 'https://the-internet.herokuapp.com/login' 
  
    # ── Locators (simpan sebagai class variable) ────── 
    USERNAME   = (By.ID,          'username') 
    PASSWORD   = (By.ID,          'password') 
    LOGIN_BTN  = (By.CSS_SELECTOR,'button[type=submit]') 
    FLASH_MSG  = (By.ID,          'flash') 
    FLASH_OK   = (By.CSS_SELECTOR,'.flash.success') 
    FLASH_ERR  = (By.CSS_SELECTOR,'.flash.error') 
 # ── Actions ─────────────────────────────────────── 
    def navigate(self): 
        self.open(self.URL) 
  
    def enter_username(self, username): 
        self.type(self.USERNAME, username) 
  
    def enter_password(self, password): 
        self.type(self.PASSWORD, password) 
  
    def click_login(self): 
        self.click(self.LOGIN_BTN) 
  
    def login(self, username, password): 
        """High-level method: 1 baris di test = 1 aksi login""" 
        self.navigate() 
        self.enter_username(username) 
        self.enter_password(password) 
        self.click_login() 
  
    # ── Assertions helpers ──────────────────────────── 
    def get_flash_message(self): 
        return self.get_text(self.FLASH_MSG) 
  
    def is_login_successful(self): 
        return self.is_visible(self.FLASH_OK) 
  
    def is_login_failed(self): 
        return self.is_visible(self.FLASH_ERR)