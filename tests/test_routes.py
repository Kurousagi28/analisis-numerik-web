import os
import sys
import unittest

# Pastikan root direktori proyek ada di sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class TestFlaskRoutes(unittest.TestCase):
    """Pengujian integrasi rute web aplikasi analisis numerik."""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_home_page(self):
        """Memastikan halaman utama dapat diakses dengan sukses (HTTP 200)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Komputasi Numerik', response.data)

    def test_metode_tabel_page(self):
        """Memastikan rute Metode Tabel dapat diakses (GET & POST)."""
        # GET
        response = self.client.get('/tabel')
        self.assertEqual(response.status_code, 200)
        # POST perhitungan default
        post_resp = self.client.post('/tabel', data={'bawah_1': '-3.0', 'atas_1': '0.0', 'n_1': '10'})
        self.assertEqual(post_resp.status_code, 200)

    def test_metode_biseksi_page(self):
        """Memastikan rute Metode Biseksi dapat diakses (GET & POST)."""
        # GET
        response = self.client.get('/biseksi')
        self.assertEqual(response.status_code, 200)
        # POST parameter biseksi
        post_resp = self.client.post('/biseksi', data={'xi': '3.0', 'xu': '5.0', 'tol': '0.5'})
        self.assertEqual(post_resp.status_code, 200)

    def test_newton_secant_page(self):
        """Memastikan rute Newton-Raphson & Secant dapat diakses (GET & POST)."""
        # GET
        response = self.client.get('/newton-secant')
        self.assertEqual(response.status_code, 200)
        # POST parameter perhitungan
        post_resp = self.client.post('/newton-secant', data={
            'x0': '0.5',
            'tol_newton': '0.0001',
            'xr_min1': '0.5',
            'xr': '10.0',
            'tol_secant': '0.0001'
        })
        self.assertEqual(post_resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
