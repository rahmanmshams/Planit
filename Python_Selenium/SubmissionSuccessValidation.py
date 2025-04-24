import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SubmissionSuccessValidation(unittest.TestCase):
    def setUp(self):
        """Set up WebDriver with window size, implicit wait, and navigate to the homepage."""
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1920, 1080)  # Set browser window size
        self.driver.implicitly_wait(60)  # Implicit wait of 60 seconds
        self.driver.get("https://jupiter.cloud.planittesting.com")
        self.wait = WebDriverWait(self.driver, 60)  # Explicit wait for specific elements

    def test_submission_form_validation(self):
        """Runs the form submission process with given data."""
        test_data_list = [
            ["Russel Stuart", "russel.stuart@test.com", "Hi, I have a product question"],
            ["David Brown", "david.brown@test.com", "Can you assist with shipping details?"],
            ["Emily White", "emily.white@test.com", "I have feedback on the site"],
            ["Michael Green", "michael.green@test.com", "What are your support hours?"],
            ["Sophia Black", "sophia.black@test.com", "Looking for partnership opportunities"]
        ]

        self.click_validate_contact_page()
        for data in test_data_list:
            print(data)
            self.enter_valid_data_mandatory_field(data)
            self.click_submit_button()
            self.validate_submission_success(data[0])
            self.click_back_button()

    def click_validate_contact_page(self):
        print('Clicking "Contact"')
        contact_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav-contact']/a")))
        contact_link.click()
        expected_url = "https://jupiter.cloud.planittesting.com/#/contact"
        self.assertEqual(self.driver.current_url, expected_url)
        print("PASS: Navigated to Contact page.")
        time.sleep(5)

    def click_submit_button(self):
        submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/form/div/a")))
        submit_button.click()
        print("EVENT: Submit button clicked.")
        time.sleep(60)

    def click_back_button(self):
        submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/a")))
        submit_button.click()
        print("EVENT: Back button clicked.")
        time.sleep(5)

    def enter_valid_data_mandatory_field(self, data):
        form_inputs = {
            "forename": ("//*[@id='forename']", data[0]),
            "email": ("//*[@id='email']", data[1]),
            "message": ("//*[@id='message']", data[2])
        }

        for field, (xpath, value) in form_inputs.items():
            input_element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            input_element.send_keys(value)
            print(f"EVENT: Entered value for {field}.")
        time.sleep(5)

    def validate_submission_success(self, name):
        success_message_xpath = "/html/body/div[2]/div/div"
        expected_success_text = f"Thanks {name}, we appreciate your feedback."
        success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, success_message_xpath)))
        self.assertEqual(success_message.text, expected_success_text)
        print(f"PASS: Success message displayed for {name}.")
        time.sleep(5)

    def tearDown(self):
        """Close the browser."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

