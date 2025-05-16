import unittest
from datetime import datetime, timedelta
from app import app, db
from models.user import User
from models.savings_goal import SavingsGoal
from models.savings_goal_share import SavingsGoalShare
from test.testConfig import BaseTestCase
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestSavingsGoalTracker(BaseTestCase):
    def setUp(self):
        super().setUp()
        logger.info("Creating test user and logging in")
        self.user = User(name='Test User', email='test@example.com', password='hashed')
        db.session.add(self.user)
        db.session.commit()

        # Simulate login by setting session
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.user.id
            sess['user_name'] = self.user.name

    def test_goal_tracker_page_load(self):
        """Test Savings Goal Tracker page load"""
        logger.info("Testing page load for /savings-goal-tracker")
        response = self.client.get('/savings-goal-tracker')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Savings Goal Tracker', response.data)
        self.assertIn(b'Your Goals', response.data)
        logger.info("✓ Page loaded with expected content")

    def test_goal_submission_redirect(self):
        """Test POST form submission"""
        logger.info("Submitting new goal")
        data = {
            'goal_name': 'Test Goal',
            'target_amount': '1000',
            'saved_amount': '250',
            'deadline': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        }
        response = self.client.post('/savings-goal-tracker', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Goal added and shared!', response.data)
        logger.info("✓ Goal submission and flash message confirmed")

    def test_goal_appears_in_own_goals(self):
        """Test a goal appears in 'Your Goals'"""
        logger.info("Creating goal manually for test")
        goal = SavingsGoal(
            user_id=self.user.id,
            goal_name='Manual Goal',
            target_amount=500,
            saved_amount=100,
            deadline=datetime.now().date()
        )
        db.session.add(goal)
        db.session.commit()

        response = self.client.get('/savings-goal-tracker')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Manual Goal', response.data)
        logger.info("✓ Manual goal appears in rendered HTML")

    def test_goal_deletion(self):
        """Test deleting a goal"""
        logger.info("Creating and deleting a goal")
        goal = SavingsGoal(
            user_id=self.user.id,
            goal_name='Delete Me',
            target_amount=300,
            saved_amount=100,
            deadline=datetime.now().date()
        )
        db.session.add(goal)
        db.session.commit()

        response = self.client.post(f'/delete-goal/{goal.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Delete Me', response.data)
        logger.info("✓ Goal deleted successfully and no longer appears")

if __name__ == '__main__':
    unittest.main()
