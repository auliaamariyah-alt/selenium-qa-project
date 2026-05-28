# tests/test_e2e_checkout.py
# Latihan 6 — Studi Kasus E-Commerce
# STMIK AMIKBANDUNG 2026

import time
import pytest
from selenium.webdriver.common.by import By
from pages.sauce_login_page import SauceDemoLoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage


class TestECommerce:

    # ── LOGIN ──────────────────────────────────────────────

    def test_TC_EC_001_login_valid(self, driver):
        """Login dengan user valid (standard_user)"""
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        assert 'inventory' in driver.current_url, \
            'Login valid harus masuk ke halaman inventory'

    def test_TC_EC_002_login_locked_user(self, driver):
        """Login dengan user yang dikunci (locked_out_user)"""
        login = SauceDemoLoginPage(driver)
        login.login('locked_out_user', 'secret_sauce')
        assert login.is_login_failed(), \
            'User yang dikunci harus mendapat pesan error'

    def test_TC_EC_003_login_invalid(self, driver):
        """Login dengan kredensial invalid"""
        login = SauceDemoLoginPage(driver)
        login.login('wronguser', 'wrongpass')
        assert login.is_login_failed(), \
            'Kredensial invalid harus mendapat pesan error'

    # ── PRODUK ─────────────────────────────────────────────

    def test_TC_EC_004_jumlah_produk(self, driver):
        """Verifikasi jumlah produk yang tampil (6 item)"""
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        assert inv.get_product_count() == 6, \
            'Harus ada 6 produk di halaman inventory'

    def test_TC_EC_005_sort_harga(self, driver):
        """Urutkan produk dari harga terendah ke tertinggi"""
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.sort_by('lohi')
        prices = inv.get_all_prices()
        assert prices == sorted(prices), \
            'Harga harus terurut dari terendah ke tertinggi'

    # ── CART ───────────────────────────────────────────────

    def test_TC_EC_006_tambah_1_produk(self, driver):
        """Tambah 1 produk ke cart, verifikasi badge = 1"""
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        assert inv.get_cart_count() == 1, \
            'Badge cart harus menunjukkan angka 1'

    def test_TC_EC_007_tambah_3_hapus_1(self, driver):
        """Tambah 3 produk, hapus 1, verifikasi badge = 2"""
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.add_product_to_cart(1)
        inv.add_product_to_cart(2)
        inv.remove_product_from_cart(0)
        assert inv.get_cart_count() == 2, \
            'Setelah hapus 1, badge cart harus menunjukkan angka 2'

    # ── CHECKOUT ───────────────────────────────────────────

    def test_TC_EC_008_checkout_berhasil(self, driver):
        """Checkout berhasil dengan data lengkap"""
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        checkout = CheckoutPage(driver)
        checkout.click_checkout()
        checkout.fill_info('Budi', 'Santoso', '40123')
        checkout.continue_checkout()
        checkout.finish_checkout()
        assert checkout.is_order_confirmed(), \
            'Order harus terkonfirmasi setelah checkout berhasil'

    def test_TC_EC_009_checkout_nama_kosong(self, driver):
        """Checkout gagal: field nama kosong"""
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        checkout = CheckoutPage(driver)
        checkout.click_checkout()
        checkout.fill_info('', '', '')
        checkout.continue_checkout()
        time.sleep(1)
        error_fields = driver.find_elements(
            By.CSS_SELECTOR, '[data-test=error]'
        )
        assert len(error_fields) > 0, \
            'Harus muncul pesan error field nama kosong'

    def test_TC_EC_010_verifikasi_total(self, driver):
        """Verifikasi total harga di confirmation page"""
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        inv.go_to_cart()
        checkout = CheckoutPage(driver)
        checkout.click_checkout()
        checkout.fill_info('Budi', 'Santoso', '40123')
        checkout.continue_checkout()
        total = checkout.get_total()
        assert 'Total' in total, \
            'Harus muncul informasi total harga'

    # ── LOGOUT ─────────────────────────────────────────────

    def test_TC_EC_011_logout(self, driver):
        """User dapat logout setelah login berhasil"""
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        inv = InventoryPage(driver)
        inv.logout()
        time.sleep(2)
        assert driver.current_url == 'https://www.saucedemo.com/', \
            'Setelah logout harus kembali ke halaman login'

    # ── END TO END ─────────────────────────────────────────

    def test_TC_EC_012_full_flow(self, driver):
        """Alur penuh: Login → Add Cart → Checkout → Logout"""
        # STEP 1 — Login
        login = SauceDemoLoginPage(driver)
        login.login('standard_user', 'secret_sauce')
        assert 'inventory' in driver.current_url

        # STEP 2 — Add to Cart
        inv = InventoryPage(driver)
        inv.add_product_to_cart(0)
        assert inv.get_cart_count() == 1

        # STEP 3 — Checkout
        inv.go_to_cart()
        checkout = CheckoutPage(driver)
        checkout.click_checkout()
        checkout.fill_info('Budi', 'Santoso', '40123')
        checkout.continue_checkout()
        checkout.finish_checkout()
        assert checkout.is_order_confirmed()

        # STEP 4 — Logout
        driver.get('https://www.saucedemo.com/inventory.html')
        time.sleep(2)
        inv2 = InventoryPage(driver)
        inv2.click(inv2.BURGER_MENU)
        time.sleep(1)
        inv2.click(inv2.LOGOUT_LINK)
        time.sleep(1)
        assert driver.current_url == 'https://www.saucedemo.com/', \
            'Setelah logout harus kembali ke halaman login'