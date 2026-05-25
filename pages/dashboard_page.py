# pages/dashboard_page.py
# Latihan 3.1 — Page Object Model
# STMIK AMIKBANDUNG 2026

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):

    URL = 'https://the-internet.herokuapp.com/secure'

    # ── Locators ──────────────────────────────────────
    LOGOUT_BTN        = (By.CSS_SELECTOR, "a[href='/logout']")
    DASHBOARD_HEADING = (By.TAG_NAME, "h2")
    FLASH_SUCCESS     = (By.CSS_SELECTOR, ".flash.success")

    # ── Actions ───────────────────────────────────────
    def logout(self):
        """Klik tombol Logout."""
        self.click(self.LOGOUT_BTN)

    # ── Assertion Helpers ─────────────────────────────
    def is_on_dashboard(self):
        """Cek apakah user sedang berada di halaman dashboard."""
        try:
            url_benar    = '/secure' in self.get_current_url()
            judul_benar  = 'Secure Area' in self.get_text(self.DASHBOARD_HEADING)
            return url_benar and judul_benar
        except:
            return False

    def is_logout_successful(self):
        """Cek apakah setelah logout user kembali ke halaman login."""
        return '/login' in self.get_current_url()