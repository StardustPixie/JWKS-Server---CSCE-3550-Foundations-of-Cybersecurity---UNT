import unittest
import requests

class TestJWKSServer(unittest.TestCase):
    def test_jwks_endpoint(self):
        response = requests.get('http://localhost:8080/.well-known/jwks.json')  # Updated URL
        self.assertEqual(response.status_code, 200)
        self.assertIn('keys', response.json())

    def test_auth_endpoint(self):
        response = requests.post('http://localhost:8080/auth')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_expired_auth_endpoint(self):
        response = requests.post('http://localhost:8080/auth?expired=true')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

if __name__ == '__main__':
    unittest.main()