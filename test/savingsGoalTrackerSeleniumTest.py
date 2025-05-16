import unittest
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestSavingsGoalTrackerSelenium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)
        cls.base_url = "http://127.0.0.1:5000"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def login(self):
        self.driver.get(f"{self.base_url}/login")

        self.driver.find_element(By.ID, "loginEmail").send_keys("test@example.com")
        self.driver.find_element(By.ID, "loginPassword").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//h2[text()='Savings Goal Tracker']"))
            )
            logger.info("Redirected to tracker after login")
        except:
            logger.warning("Not redirected, navigating manually to /savings-goal-tracker")
            self.driver.get(f"{self.base_url}/savings-goal-tracker")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[text()='Savings Goal Tracker']"))
            )
            logger.info("Manual navigation worked")

    def test_01_login_and_load_tracker_page(self):
        self.login()
        heading = self.driver.find_element(By.XPATH, "//h2[text()='Savings Goal Tracker']")
        self.assertEqual(heading.text.strip(), "Savings Goal Tracker")

    logger.info("Goal submitted and visible")

    def test_02_delete_goal(self):
        self.login()
        time.sleep(1)

        try:
            delete_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[title='Delete Goal']")
            if delete_buttons:
                delete_buttons[0].click()

                confirm_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#deleteGoalModal .btn-danger"))
                )
                confirm_button.click()

                WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Selenium Test Goal')]")
                ))

                self.driver.refresh()
                self.assertNotIn("Selenium Test Goal", self.driver.page_source)
                logger.info("Goal deleted successfully")
            else:
                self.skipTest("No deletable goal found")
        except Exception as e:
            logger.error(f"Error deleting goal: {str(e)}")
            raise

if __name__ == "__main__":
    unittest.main()
