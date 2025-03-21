import unittest
from myapp import create_app
import jwt
import time

class TestJWKSServer(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_jwks_endpoint(self):
        response = self.app.get('/.well-known/jwks.json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('keys', response.json)

    def test_auth_endpoint(self):
        response = self.app.post('/auth')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        token = response.json['token']
        decoded = jwt.decode(token, options={"verify_signature": False})
        self.assertIn('exp', decoded)

    def test_expired_auth_endpoint(self):
        response = self.app.post('/auth?expired=true')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        token = response.json['token']
        decoded = jwt.decode(token, options={"verify_signature": False})
        self.assertLess(decoded['exp'], time.time())

if __name__ == '__main__':
    unittest.main()
