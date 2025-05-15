import sys
import os
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test.testConfig import BaseTestCase

# add project root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAuthSelenium(BaseTestCase):
    # shared test user information
    TEST_USERNAME = "seleniumuser"
    TEST_EMAIL = "selenium@example.com"
    TEST_PASSWORD = "password123"
    
    @classmethod
    def setUpClass(cls):
        """start flask server before all tests"""
        cls.server_thread = threading.Thread(target=cls.run_flask_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2) # wait for server to start
    
    @classmethod
    def run_flask_server(cls):
        """run flask server in a thread"""
        from app import app
        app.config['TESTING'] = True
        app.run(host='127.0.0.1', port=5000, use_reloader=False, debug=False)
    
    def setUp(self):
        """prepare for each test"""
        super().setUp() # this will call BaseTestCase.setUp(), which contains db.create_all()
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
    
    def tearDown(self):
        """clean up after each test"""
        if self.driver:
            self.driver.quit()
        super().tearDown() # this will call BaseTestCase.tearDown(), which contains db.drop_all()
    
    def test_1_register(self):
        """test user registration"""
        self.driver.get("http://127.0.0.1:5000/login")
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "login-form")))
        
        self.driver.find_element(By.ID, "signup-tab").click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "signup-form")))
        
        self.driver.find_element(By.ID, "signupName").send_keys(self.TEST_USERNAME)
        self.driver.find_element(By.ID, "signupEmail").send_keys(self.TEST_EMAIL)
        self.driver.find_element(By.ID, "signupPassword").send_keys(self.TEST_PASSWORD)
        self.driver.find_element(By.ID, "confirmPassword").send_keys(self.TEST_PASSWORD)
        
        agree_terms = self.driver.find_element(By.ID, "agreeTerms")
        self.driver.execute_script("arguments[0].click();", agree_terms)
        
        submit_button = self.driver.find_element(By.XPATH, "//div[@id='signup-form']//button[@type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert') and contains(text(), 'registration successful')]"))
        )
        self.assertIsNotNone(success_message)
        print(f"test_1_register: {self.TEST_EMAIL}")
    
    def test_2_login_registered_user(self):
        """test login for registered user"""
        # step 1: use API to ensure user exists in current test database
        # (BaseTestCase's setUp/tearDown will clean up and rebuild database for each test)
        register_response = self.client.post(
            '/register',
            data={
                'signupName': self.TEST_USERNAME,
                'signupEmail': self.TEST_EMAIL,
                'signupPassword': self.TEST_PASSWORD,
                'confirmPassword': self.TEST_PASSWORD
            },
            follow_redirects=True
        )
        # confirm API registration success, usually redirect to login page and has success message
        self.assertEqual(register_response.status_code, 200) 
        self.assertIn(b'registration successful', register_response.data)
        print(f"test_2_login_registered_user: {self.TEST_EMAIL}")

        # step 2: login through selenium UI
        self.driver.get("http://127.0.0.1:5000/login")
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "login-form")))
        
        self.driver.find_element(By.ID, "loginEmail").send_keys(self.TEST_EMAIL)
        self.driver.find_element(By.ID, "loginPassword").send_keys(self.TEST_PASSWORD)
        
        submit_button = self.driver.find_element(By.XPATH, "//div[@id='login-form']//button[@type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        WebDriverWait(self.driver, 10).until(EC.url_contains("dashboard"))
        self.assertTrue("dashboard" in self.driver.current_url)
        print(f"test_2_login_registered_user: {self.TEST_EMAIL}")

    def test_3_login_invalid_credentials(self):
        """test login with invalid credentials"""
        self.driver.get("http://127.0.0.1:5000/login")
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "login-form")))
        
        self.driver.find_element(By.ID, "loginEmail").send_keys("wrong@example.com")
        self.driver.find_element(By.ID, "loginPassword").send_keys("wrongpassword")
        
        submit_button = self.driver.find_element(By.XPATH, "//div[@id='login-form']//button[@type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(submit_button))
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert') and contains(text(), 'login failed')]"))
        )
        self.assertIsNotNone(error_message)
        print(f"test_3_login_invalid_credentials: {self.TEST_EMAIL}")
