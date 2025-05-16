import json
import sys
import os
import pandas as pd
from test.testConfig import BaseTestCase
from flask import session
from models.user import User
from werkzeug.security import generate_password_hash
from db import db


# Add project root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestPersonality(BaseTestCase):
    def setUp(self):
        # Register a test user and log in
        super().setUp()
        # Create a test user in database
        user = User(name='personality',
                    email='personality@example.com',
                    password='123')

        db.session.add(user)
        db.session.commit()

        # Login with the test user
        response = self.client.post(
            '/login',
            data={
                'loginEmail': 'personality@example.com',
                'loginPassword': '123'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)  

    def create_valid_excel(self, filename):
        # Create a valid Excel file for testing
        data = {
            'Date': ['2025-05-01'],
            'Category': ['Food'],
            'Description': ['Lunch'],
            'Amount': [12.5],
            'Payment Method': ['Credit Card']
        }
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)

    def test_personality_page_load(self):
        # Test if spending personality analyzer page loads
        response = self.client.get('/spending-personality-analyzer', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Spending Personality Analyzer', response.data)

    def test_valid_file_upload(self):
        # Test uploading valid excel file
        file_path = 'test_data.xlsx'
        self.create_valid_excel(file_path)
    
        with open(file_path, 'rb') as file:
            response = self.client.post(
                '/spending-personality-analyzer',
                data={'file': (file, 'test_data.xlsx')},
                content_type='multipart/form-data',
                follow_redirects=True
            )

        os.remove('test_data.xlsx')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Spending Personality', response.data)

    def test_invalid_file_upload(self):
        # Test uploading invalid type of file
        # Create a fake non-Excel file
        file_path = 'test_data.txt'
        with open(file_path, 'w') as f:
            f.write('Sample invalid data for testing')  # Write as a string, not bytes

        # Open and upload the file
        with open(file_path, 'rb') as f:
            response = self.client.post(
                '/spending-personality-analyzer',
                data={'file': (f, 'test_data.txt')},
                content_type='multipart/form-data'
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please upload a valid Excel (.xlsx) file.', response.data)

        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_empty_file_upload(self):
        filename = 'empty.xlsx'
       # Test uploading an empty file
        with open('empty.xlsx', 'wb') as f:
            pass
        
        with open('empty.xlsx', 'rb') as file:
            response = self.client.post(
                '/spending-personality-analyzer',
                data={'file': (file, filename)},
                content_type='multipart/form-data',
                follow_redirects=True
            )
        if os.path.exists(filename):
            os.remove('empty.xlsx')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error processing file', response.data)

    def test_results_display(self):
        # Test if analysis results are displayed after upload
        filename = 'test_data.xlsx'
        self.create_valid_excel(filename)

        with open('test_data.xlsx', 'rb') as file:
            response = self.client.post(
                '/spending-personality-analyzer',
                data={'file': (file, 'test_data.xlsx')},
                content_type='multipart/form-data',
                follow_redirects=True
            )
        os.remove('test_data.xlsx')  # Clean up

        self.assertEqual(response.status_code, 200)
        # Check for results displaying in the response data
        self.assertIn(b'Spending Personality Analyzer', response.data)
        self.assertIn(b'Your Spending Personality: ', response.data)

        # Check for the bar chart to ensure it was rendered
        self.assertIn(b'id="barChart"', response.data)
        self.assertIn(b'Your Spending vs Your Personality Group Average', response.data)

    def test_analyze_again_button(self):
        # Access the spending personality analyzer page
        response = self.client.get('/spending-personality-analyzer')

        # Convert response data to text for easy matching
        response_text = response.data.decode('utf-8')

        # Check if the "Analyze Again" button text is present (considering emoji and spacing)
        self.assertIn('⬅ Back to Toolkit', response_text)
        self.assertIn('📈 Upload & Visualize', response_text)

if __name__ == '__main__':
    import unittest
    unittest.main()