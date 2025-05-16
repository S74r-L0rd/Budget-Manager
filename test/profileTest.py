import json
import sys
import os
from test.testConfig import BaseTestCase
from flask import session

# Add project root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the path to the test files
TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'test_files')

class TestAuth(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Register and login a test user before profile tests
        self.client.post(
            '/register',
            data={
                'signupName': 'profileuser',
                'signupEmail': 'profile@example.com',
                'signupPassword': '123',
                'confirmPassword': '123'
            }
        )
        self.client.post(
            '/login',
            data={
                'loginEmail': 'profile@example.com',
                'loginPassword': '123'
            }
        )

    def test_profile_load(self):
        # Test if profile page loads successfully
        response = self.client.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile', response.data)

    def test_profile_update(self):
        # Test profile update
        response = self.client.post(
            '/update-prof',
            data={
                'name': 'Updated Profile',
                'email': 'profile@example.com',
                'phone': '11111111',
                'address': '123 Updated St',
                'dob': '2000-01-01',
                'gender': 'Male',
                'occupation': 'Student'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile updated successfully', response.data)

    def test_profile_photo_upload(self):
        # Test uploading a valid profile photo
        with open(os.path.join(TEST_FILES_DIR, 'test.png'), 'rb') as png:
            response = self.client.post(
                '/upload-photo',
                data={'photo': (png, 'test.png')},
                content_type='multipart/form-data',
                follow_redirects=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile photo updated successfully!', response.data)

    def test_invalid_profile_photo_upload(self):
        # Test uploading an invalid profile photo extension
        with open(os.path.join(TEST_FILES_DIR, 'test.txt'), 'rb') as txt:
            response = self.client.post(
                '/upload-photo',
                data={'photo': (txt, 'test.txt')},
                content_type='multipart/form-data',
                follow_redirects=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid file type. Please upload an image.', response.data)

    def test_delete_profile_photo(self):
       # Test deleting the profile photo
        with open(os.path.join(TEST_FILES_DIR, 'test.png'), 'rb') as png:
            self.client.post(
                '/upload-photo',
                data={'photo': (png, 'test.png')},
                content_type='multipart/form-data',
                follow_redirects=True
            )

        # Delete the uploaded photo
        response = self.client.post(
            '/delete-photo',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile photo has been reset to the default image.', response.data)

    def test_password_update(self):
        # Test updating password
        response = self.client.post(
            '/change_password',
            data={
                'current_password': '123',
                'new_password': '12345',
                'confirm_password': '12345'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password successfully updated', response.data)

        # Log out after updating
        self.client.get('/logout')

        # Log in again with updated password
        response = self.client.post(
            '/login',
            data={
                'loginEmail': 'profile@example.com',
                'loginPassword': '12345'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hi, profileuser', response.data)

    def test_delete_account(self):
        # Test deleting the user account
        response = self.client.post(
            '/delete_account',
            data={'confirm': 'DELETE'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been deleted successfully.', response.data)

        # Try logging in after account deletion
        response = self.client.post(
            '/login',
            data={
                'loginEmail': 'profile@example.com',
                'loginPassword': '123'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login failed, please check your email or password', response.data)

# Commented out for now to keep the testing files for repitition
    # def cleanup_test_files(self):    
    #     if os.path.exists(os.path.join(TEST_FILES_DIR, 'test.png')):
    #         os.remove(os.path.join(TEST_FILES_DIR, 'test.png'))

if __name__ == '__main__':
    import unittest
    unittest.main()