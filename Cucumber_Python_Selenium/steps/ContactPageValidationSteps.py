from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@given("the user navigates to the Contact page")
def step_navigate_to_contact_page(context):
    context.driver = webdriver.Chrome()
    context.driver.set_window_size(1920, 1080)
    context.driver.implicitly_wait(10)
    context.driver.get("https://jupiter.cloud.planittesting.com")
    contact_link = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav-contact']/a")))
    contact_link.click()
    time.sleep(5)
    assert context.driver.current_url == "https://jupiter.cloud.planittesting.com/#/contact"
    print("PASS: Navigated to Contact page.")

@when("the user clicks the Submit button without filling the form")
def step_click_submit_button(context):
    submit_button = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/form/div/a")))
    time.sleep(5)
    submit_button.click()
    print("EVENT: Submit button clicked.")

@then("validation error messages appear for mandatory fields")
def step_validate_errors(context):
    error_messages = {
        "forename": ("//*[@id='forename-err']", "Forename is required"),
        "email": ("//*[@id='email-err']", "Email is required"),
        "message": ("//*[@id='message-err']", "Message is required")
    }
    for field, (xpath, expected_msg) in error_messages.items():
        error_element = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        assert error_element.text == expected_msg
    time.sleep(5)

@when("the user fills mandatory fields with valid data")
def step_fill_mandatory_fields(context):
    for row in context.table:
        form_inputs = {
            "forename": ("//*[@id='forename']", row["Forename"]),
            "email": ("//*[@id='email']", row["Email"]),
            "message": ("//*[@id='message']", row["Message"])
        }
        for field, (xpath, value) in form_inputs.items():
            input_element = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            input_element.send_keys(value)
            print(f"EVENT: Entered value for {field}.")
    time.sleep(5)

@when("the user clicks the Submit button")
def step_click_submit_button_again(context):
    submit_button = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/form/div/a")))
    submit_button.click()
    time.sleep(60)
    print("EVENT: Submit button clicked.")

@then('the success message "{expected_message}" is displayed')
def step_validate_submission_success(context, expected_message):
    success_message_xpath = "/html/body/div[2]/div/div"
    success_message = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, success_message_xpath)))
    assert success_message.text == expected_message, f"Expected '{expected_message}', but got '{success_message.text}'"
    print(f"PASS: Success message displayed: {success_message.text}")
    context.driver.quit()

@then("the validation error messages disappear")
def step_validate_no_errors(context):
    error_fields = ["//*[@id='forename-err']", "//*[@id='email-err']", "//*[@id='message-err']"]
    for xpath in error_fields:
        WebDriverWait(context.driver, 10).until_not(EC.presence_of_element_located((By.XPATH, xpath)))
    context.driver.quit()
