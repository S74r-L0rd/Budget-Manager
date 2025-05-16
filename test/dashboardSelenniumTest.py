import unittest
import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from werkzeug.security import generate_password_hash
from db import db
from models.user import User
from test.testConfig import BaseTestCase
from app import app

class DashboardSeleniumTest(BaseTestCase):
    
    @classmethod
    def setUpClass(cls):
        # use port 5001, avoid conflict with macOS AirPlay
        port = 5001
        # start Flask server in a separate thread
        cls.server_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port))
        cls.server_thread.daemon = True
        cls.server_thread.start()
        print(f"Starting test server on port {port}...")
        time.sleep(3)  # give server more startup time
        
        # set Chrome browser to headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080") # add window size parameter
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.port = port
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print("Test completed, closing browser...")
    
    def setUp(self):
        super().setUp()
        
        # create test user
        test_user = User(
            email="test@example.com",
            name="Test User",
            password="password123"
        )
        db.session.add(test_user)
        db.session.commit()
        print(f"Created test user: {test_user.email}")
    
    def test_dashboard_access(self):
        try:
            # access login page using correct port
            login_url = f"http://localhost:{self.port}/login"
            print(f"Accessing login page: {login_url}")
            self.driver.get(login_url)
            
            # wait for page load
            time.sleep(3)
            
            # print current status, help debug
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page title: {self.driver.title}")
            
            # print full page source code, help debug
            page_source = self.driver.page_source
            print(f"Page source code first 1000 characters: {page_source[:1000]}...")
            
            # check if page contains login form
            if "loginEmail" not in page_source and "loginPassword" not in page_source:
                print("Warning: Login form elements not found on the page!")
                self.driver.save_screenshot("login_form_missing.png")
                print("Login page screenshot saved: login_form_missing.png")
            
            # locate form first, then find elements in the form
            wait = WebDriverWait(self.driver, 15)
            form = wait.until(EC.presence_of_element_located((By.XPATH, "//form[@action='/login' or contains(@id, 'login')]")))
            print("Found login form")
            
            # find input fields in the form
            email_input = form.find_element(By.XPATH, ".//input[@type='email' or @id='loginEmail' or @name='loginEmail']")
            password_input = form.find_element(By.XPATH, ".//input[@type='password' or @id='loginPassword' or @name='loginPassword']")
            submit_button = form.find_element(By.XPATH, ".//button[@type='submit']")
            
            print("Found all form elements")
            
            # fill in login form
            email_input.send_keys("test@example.com")
            password_input.send_keys("password123")
            
            # submit login form
            submit_button.click()
            print("Submitted login form")
            
            # wait for redirect to dashboard
            dashboard_url = f"http://localhost:{self.port}/dashboard"
            wait.until(
                EC.url_contains("/dashboard")
            )
            
            # simple verification - as long as the dashboard page is accessible, it is successful
            current_url = self.driver.current_url
            print(f"After login, URL: {current_url}")
            self.assertTrue("/dashboard" in current_url, "Failed to redirect to dashboard page")
            
            print("Login test successful! User can access dashboard page.")
            
        except Exception as e:
            # save screenshot, help debug
            self.driver.save_screenshot("test_error.png")
            print(f"Error details: {str(e)}")
            print(f"Screenshot saved as test_error.png")
            raise e

if __name__ == "__main__":
    unittest.main()
