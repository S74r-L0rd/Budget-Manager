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

class TestContactSelenium(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Starting Flask server for tests")
        cls.server_thread = threading.Thread(target=cls.run_flask_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)
        logger.info("Flask server started successfully")

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
        logger.info("Chrome WebDriver initialized successfully")

    def tearDown(self):
        if self.driver:
            logger.info("Closing Chrome WebDriver")
            self.driver.quit()
        super().tearDown()
        logger.info("Test cleanup completed")

    def test_contact_form_submission(self):
        logger.info("Starting contact form submission test")
        self.driver.get("http://127.0.0.1:5000/contact")
        
        logger.info("Waiting for contact form to be visible")
        contact_form = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "contactForm"))
        )
        logger.info("✓ Contact form found")
        
        # Fill out form fields
        form_data = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "message": "This is a test message"
        }
        
        logger.info("Filling out form fields")
        for field_id, value in form_data.items():
            field = self.driver.find_element(By.ID, field_id)
            field.clear()
            field.send_keys(value)
            logger.info(f"✓ Filled {field_id} with value: {value}")

        logger.info("Submitting form")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "#contactForm button[type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        logger.info("Waiting for success alert")
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        self.assertIn("Message sent successfully!", alert_text)
        logger.info(f"✓ Success alert received: {alert_text}")
        alert.accept()
        logger.info("Contact form submission test completed successfully")

    def test_smooth_scroll_to_faq(self):
        logger.info("Starting FAQ scroll test")
        self.driver.get("http://127.0.0.1:5000/contact")
        
        logger.info("Looking for FAQ button")
        faq_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-target='faq']"))
        )
        logger.info("✓ FAQ button found")
        
        logger.info("Clicking FAQ button")
        self.driver.execute_script("arguments[0].click();", faq_button)
        
        logger.info("Waiting for scroll animation")
        time.sleep(2)
        
        logger.info("Checking FAQ section visibility")
        faq_section = self.driver.find_element(By.ID, "faq")
        is_visible = self.driver.execute_script("""
            const elem = arguments[0];
            const rect = elem.getBoundingClientRect();
            const windowHeight = window.innerHeight || document.documentElement.clientHeight;
            return (
                rect.top >= 0 &&
                rect.bottom <= windowHeight
            );
        """, faq_section)
        
        self.assertTrue(is_visible, "FAQ section should be visible in viewport")
        logger.info("✓ FAQ section is visible in viewport")
        logger.info("FAQ scroll test completed successfully")

    def test_smooth_scroll_to_contact_form(self):
        logger.info("Starting contact form scroll test")
        self.driver.get("http://127.0.0.1:5000/contact")
        
        logger.info("Looking for Contact Us button")
        contact_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-target='contact-form']"))
        )
        logger.info("✓ Contact Us button found")
        
        logger.info("Clicking Contact Us button")
        self.driver.execute_script("arguments[0].click();", contact_button)
        
        logger.info("Waiting for scroll animation")
        time.sleep(2)
        
        logger.info("Checking contact form visibility")
        contact_form = self.driver.find_element(By.ID, "contact-form")
        is_visible = self.driver.execute_script("""
            const elem = arguments[0];
            const rect = elem.getBoundingClientRect();
            const windowHeight = window.innerHeight || document.documentElement.clientHeight;
            return (
                rect.top >= 0 &&
                rect.bottom <= windowHeight
            );
        """, contact_form)
        
        self.assertTrue(is_visible, "Contact form section should be visible in viewport")
        logger.info("✓ Contact form is visible in viewport")
        logger.info("Contact form scroll test completed successfully")