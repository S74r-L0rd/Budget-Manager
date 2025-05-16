import json
import sys
import os
import logging
from test.testConfig import BaseTestCase
from unittest.mock import patch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Add project root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestContact(BaseTestCase):
    def test_contact_page_load(self):
        """Test if contact page loads successfully"""
        logger.info("Starting contact page load test")
        
        response = self.client.get('/contact')
        logger.info(f"Got response with status code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        logger.info("Checking for required elements in page content")
        
        required_elements = [
            (b'Get in Touch With Us', "Hero title"),
            (b'Contact Us', "Contact section title"),
            (b'id="contactForm"', "Contact form"),
            (b'id="faq"', "FAQ section")
        ]
        
        for content, element_name in required_elements:
            if content in response.data:
                logger.info(f"✓ Found {element_name}")
            else:
                logger.warning(f"✗ Missing {element_name}")
            self.assertIn(content, response.data)
        
        logger.info("Contact page load test completed successfully")

    @patch('app.getenv')
    def test_emailjs_config_api(self, mock_getenv):
        """Test if EmailJS config API returns correct data"""
        logger.info("Starting EmailJS config API test")
        
        # Mock environment variables
        mock_vars = {
            'EMAILJS_SERVICE_ID': 'test_service',
            'EMAILJS_TEMPLATE_ID': 'test_template',
            'EMAILJS_PUBLIC_KEY': 'test_public_key'
        }
        logger.info(f"Setting up mock environment variables: {list(mock_vars.keys())}")
        mock_getenv.side_effect = lambda x: mock_vars.get(x)

        logger.info("Making request to EmailJS config API")
        response = self.client.get('/api/emailjs-config')
        logger.info(f"Got response with status code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        logger.info(f"Received config data with keys: {list(data.keys())}")
        
        # Verify all required fields
        required_fields = ['serviceId', 'templateId', 'publicKey']
        for field in required_fields:
            if field in data:
                logger.info(f"✓ Found {field} in response")
            else:
                logger.warning(f"✗ Missing {field} in response")
            self.assertIn(field, data)
        
        # Verify values
        self.assertEqual(data['serviceId'], 'test_service')
        logger.info("EmailJS config API test completed successfully")