# tests/test_logout.py

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class TestLogout:

    def test_login_lalu_logout_kembali_ke_halaman_login(self, login_page):
        # STEP 1 — Login dengan kredensial valid
        login_page.login('tomsmith', 'SuperSecretPassword!')

        # STEP 2 — Verifikasi user masuk ke dashboard
        dashboard = DashboardPage(login_page.driver)
        assert dashboard.is_on_dashboard(), \
            'Setelah login, user harus berada di halaman Dashboard'

        # STEP 3 — Lakukan logout
        dashboard.logout()

        # STEP 4 — Verifikasi kembali ke halaman login
        assert dashboard.is_logout_successful(), \
            'Setelah logout, user harus kembali ke halaman /login'

    def test_heading_secure_area_muncul_setelah_login(self, login_page):
        login_page.login('tomsmith', 'SuperSecretPassword!')

        dashboard = DashboardPage(login_page.driver)
        assert dashboard.is_on_dashboard(), \
            'Heading Secure Area harus muncul setelah login berhasil'