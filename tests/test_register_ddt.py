# tests/test_register_ddt.py
# Latihan 4.1 — Data Driven Testing
# STMIK AMIKBANDUNG 2026

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from tests.conftest import load_csv


class TestRegisterDDT:

    @pytest.mark.parametrize(
        'row',
        load_csv('register_data.csv')
    )
    def test_register_from_csv(self, driver, row):
        wait = WebDriverWait(driver, 30)

        # Buka halaman register
        driver.get('https://demoqa.com/register')

        # Tunggu halaman loaded
        wait.until(EC.presence_of_element_located((By.ID, 'firstname')))

        # Fungsi bantu isi field
        def isi(field_id, value):
            if value:
                el = wait.until(
                    EC.presence_of_element_located((By.ID, field_id))
                )
                el.clear()
                el.send_keys(value)

        # Isi semua field dari data CSV
        isi('firstname', row['firstname'])
        isi('lastname',  row['lastname'])
        isi('userName',  row['username'])
        isi('password',  row['password'])

        # Klik tombol Register
        wait.until(EC.element_to_be_clickable((By.ID, 'register'))).click()

        # Tunggu sebentar setelah klik
        time.sleep(2)

        # Cek error — bisa berupa field is-invalid ATAU alert popup
        error_fields = driver.find_elements(By.CSS_SELECTOR, '.is-invalid')
        ada_field_error = len(error_fields) > 0

        # Cek juga alert popup
        ada_alert = False
        try:
            alert = driver.switch_to.alert
            alert.accept()  # tutup alert
            ada_alert = True
        except NoAlertPresentException:
            ada_alert = False

        ada_error = ada_field_error or ada_alert

        # Evaluasi hasil
        if row['expected'] == 'PASS':
            assert not ada_error, \
                f"[{row['description']}] Registrasi seharusnya BERHASIL"
        else:  # FAIL
            assert ada_error, \
                f"[{row['description']}] Registrasi seharusnya DITOLAK"