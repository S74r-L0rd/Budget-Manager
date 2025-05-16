import unittest
from app import app

class TestToolsPage(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_tools_page_loads(self):
        response = self.client.get('/tools')  # 🔁 Update if your route is different
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Smarter Tools for Smarter Finance', response.data)
        self.assertIn(b'Explore Our Tools', response.data)

    def test_tools_content_present(self):
        response = self.client.get('/tools')
        # Check for key tool names
        self.assertIn(b'Expense Tracker', response.data)
        self.assertIn(b'Budget Planner', response.data)
        self.assertIn(b'Savings Goal Tracker', response.data)
        self.assertIn(b'Future Expense Predictor', response.data)
        self.assertIn(b'Spending Personality Analyzer', response.data)
        self.assertIn(b'Expense Splitter', response.data)

        # Check for 'How It Works' section
        self.assertIn(b'How It Works', response.data)
        self.assertIn(b'Upload Data', response.data)
        self.assertIn(b'Visualize Trends', response.data)

    def tearDown(self):
        pass  # No cleanup needed since we’re not hitting the DB

if __name__ == '__main__':
    unittest.main()
