import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MandatoryFieldValidation(unittest.TestCase):
    def setUp(self):
        """Set up WebDriver with window size, implicit wait, and navigate to the homepage."""
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1920, 1080)  # Set browser window size
        self.driver.implicitly_wait(10)  # Implicit wait of 10 seconds
        self.driver.get("http://jupiter.cloud.planittesting.com")
        self.wait = WebDriverWait(self.driver, 10)  # Explicit wait for specific elements
        self.error_messages = {
            "forename": ("//*[@id='forename-err']", "Forename is required"),
            "email": ("//*[@id='email-err']", "Email is required"),
            "message": ("//*[@id='message-err']", "Message is required")
        }

    def test_mandatory_field_validation(self):
        self.click_validate_contact_page()
        self.click_submit_button()
        self.validate_error_msg_mandatory_field()
        self.enter_valid_data_mandatory_field(["David Jones", "david.jones@test.com", "Hi this is David here"])
        self.validate_no_error_msg_mandatory_field()

    def click_validate_contact_page(self):
        # Click on Contact (using explicit wait)
        print('Clicking "Contact"')
        contact_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav-contact']/a")))
        contact_link.click()

        # Validate URL
        print('Validating opened URL to expected one')
        expected_url = "https://jupiter.cloud.planittesting.com/#/contact"
        self.assertEqual(self.driver.current_url, expected_url)
        print("PASS: Navigated to Contact page.")
        time.sleep(1)

    def click_submit_button(self):
        # Click Submit button (using explicit wait)
        submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/form/div/a")))
        submit_button.click()
        print("EVENT: Submit button clicked.")
        time.sleep(1)

    def validate_error_msg_mandatory_field(self):
        # Validate error messages for mandatory fields (using explicit wait)
        for field, (xpath, expected_msg) in self.error_messages.items():
            error_element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.assertEqual(error_element.text, expected_msg)
            print(f"PASS: Validation message for {field} is correct.")

        time.sleep(1)

    def enter_valid_data_mandatory_field(self, data):
        # Fill mandatory fields with values (using explicit wait)
        form_inputs = {
            "forename": ("//*[@id='forename']", data[0]),
            "email": ("//*[@id='email']", data[1]),
            "message": ("//*[@id='message']", data[2])
        }

        for field, (xpath, value) in form_inputs.items():
            input_element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            input_element.send_keys(value)
            print(f"EVENT: Entered value for {field}.")

        time.sleep(1)

    def validate_no_error_msg_mandatory_field(self):
        for field, (xpath, _) in self.error_messages.items():
            # Using `find_elements` in case error disappears completely
            self.wait.until_not(EC.presence_of_element_located((By.XPATH, xpath)))
            print(f"PASS: No validation errors for {field}.")

    def tearDown(self):
        """Close the browser."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
