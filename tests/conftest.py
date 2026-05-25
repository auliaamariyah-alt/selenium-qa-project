# tests/conftest.py
import pytest
import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# ── Fixture driver (modul hal.9) ──────────────────────────
@pytest.fixture(scope='function')
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    d = webdriver.Chrome(
        service=Service(r'C:\chromedriver-win64\chromedriver.exe'),
        options=options
    )
    d.set_page_load_timeout(60)  # tunggu max 60 detik untuk load halaman
    yield d
    d.quit()


@pytest.fixture(scope='function')
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)


# ── Fungsi baca CSV (modul hal.12) ────────────────────────
def load_csv(filename):
    """Baca file CSV dari folder data/ dan kembalikan sebagai list of dict"""
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


# ── Screenshot otomatis saat FAIL (modul hal.12-13) ───────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            os.makedirs('reports/screenshots', exist_ok=True)
            name = item.nodeid.replace('/', '_').replace('::', '_')
            driver.save_screenshot(f'reports/screenshots/{name}.png')
            print(f'\nScreenshot disimpan: {name}.png')