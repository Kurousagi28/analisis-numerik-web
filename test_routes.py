import unittest
from app import app

class FlaskRoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_tabel_route_get(self):
        response = self.client.get('/tabel')
        self.assertEqual(response.status_code, 200)

    def test_biseksi_route_get(self):
        response = self.client.get('/biseksi')
        self.assertEqual(response.status_code, 200)

    def test_newton_secant_route_get(self):
        response = self.client.get('/newton-secant')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
