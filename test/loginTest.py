import json
import sys
import os
from test.testConfig import BaseTestCase
from flask import session

# add project root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAuth(BaseTestCase):
    def test_register(self):
        # test register new user
        response = self.client.post(
            '/register',
            data={
                'signupName': 'testuser',
                'signupEmail': 'test@example.com',
                'signupPassword': 'password123',
                'confirmPassword': 'password123'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        # check if registration successful message is displayed
        self.assertIn(b'registration successful', response.data)

    def test_login(self):
        # register user first
        self.client.post(
            '/register',
            data={
                'signupName': 'testuser',
                'signupEmail': 'test@example.com',
                'signupPassword': 'password123',
                'confirmPassword': 'password123'
            }
        )

        # test login
        response = self.client.post(
            '/login',
            data={
                'loginEmail': 'test@example.com',
                'loginPassword': 'password123'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        # after login, should be redirected to dashboard
        self.assertIn(b'dashboard', response.data)

    def test_login_invalid_credentials(self):
        # test login with invalid credentials
        response = self.client.post(
            '/login',
            data={
                'loginEmail': 'wrong@example.com',
                'loginPassword': 'wrongpassword'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        # check if login failed message is displayed
        self.assertIn(b'login failed', response.data)
