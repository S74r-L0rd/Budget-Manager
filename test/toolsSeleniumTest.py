import sys
import os
import time
import threading
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test.testConfig import BaseTestCase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class TestToolsSelenium(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        """Start flask server before all tests"""
        logger.info("Starting Flask server for tests")
        cls.server_thread = threading.Thread(target=cls.run_flask_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)
        logger.info("✓ Flask server started")

    @classmethod
    def run_flask_server(cls):
        from app import app
        app.config['TESTING'] = True
        app.run(host='127.0.0.1', port=5000, use_reloader=False, debug=False)

    def setUp(self):
        super().setUp()
        logger.info("Setting up Chrome WebDriver")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        logger.info("✓ Chrome WebDriver initialized")

    def test_explore_tools_button_scroll(self):
        """Test if 'Explore Tools' button scrolls to tool list section"""
        logger.info("Starting explore tools button scroll test")
        self.driver.get("http://127.0.0.1:5000/tools")
        
        # Find and click Explore Tools button
        explore_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#tool-list']"))
        )
        logger.info("✓ Found Explore Tools button")
        
        self.driver.execute_script("arguments[0].click();", explore_button)
        logger.info("✓ Clicked Explore Tools button")
        
        # Wait for scroll animation
        time.sleep(2)
        
        # Check if tool list section is visible
        tool_list = self.driver.find_element(By.ID, "tool-list")
        is_visible = self.driver.execute_script("""
            const elem = arguments[0];
            const rect = elem.getBoundingClientRect();
            const windowHeight = window.innerHeight || document.documentElement.clientHeight;
            return (
                rect.top >= 0 &&
                rect.bottom <= windowHeight
            );
        """, tool_list)
        
        self.assertTrue(is_visible, "Tool list section should be visible in viewport")
        logger.info("✓ Tool list section is visible")

    def test_get_started_navigation(self):
        """Test if 'Get Started' button navigates to login page"""
        logger.info("Starting get started button navigation test")
        self.driver.get("http://127.0.0.1:5000/tools")
        
        # Find and click Get Started button
        get_started_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".learn-more-btn"))
        )
        logger.info("✓ Found Get Started button")
        
        get_started_button.click()
        logger.info("✓ Clicked Get Started button")
        
        # Verify navigation to login page
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/login")
        )
        self.assertIn("/login", self.driver.current_url)
        logger.info("✓ Successfully navigated to login page")

    def tearDown(self):
        if self.driver:
            self.driver.quit()
            logger.info("✓ Browser closed")
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        logger.info("✓ All tests completed")