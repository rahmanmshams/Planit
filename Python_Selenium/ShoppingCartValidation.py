import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ShoppingCartValidation(unittest.TestCase):
    def setUp(self):
        """Set up WebDriver with window size and implicit wait."""
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(10)
        self.driver.get("https://jupiter.cloud.planittesting.com")
        self.wait = WebDriverWait(self.driver, 10)
        self.item = { ''
                      'Teddy Bear': {'item_code': '1', 'price': ''}, 'Stuffed Frog': {'item_code': '2', 'price': ''},
                      'Handmade Doll': {'item_code': '3', 'price': ''}, 'Fluffy Bunny': {'item_code': '4', 'price': ''},
                      'Smiley Bear': {'item_code': '5', 'price': ''}, 'Funny Cow': {'item_code': '6', 'price': ''},
                      'Valentine Bear': {'item_code': '7', 'price': ''}, 'Smiley Face': {'item_code': '8', 'price': ''}
                      }

    def test_shopping_cart_validation(self):
        shopping_list = {'Stuffed Frog': 2, 'Fluffy Bunny': 5, 'Valentine Bear': 3}
        cart_count = 0
        self.click_validate_shop_page()
        for item in shopping_list:
            cart_count += shopping_list[item]
            self.purchase_item(item, shopping_list[item], cart_count)
        self.click_validate_cart_page()
        self.validate_cart(shopping_list)

    def click_validate_shop_page(self):
        # Click on Shop
        shop_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav-shop']/a")))
        shop_link.click()
        print("EVENT: Navigated to Shop page.")

        # Validate URL
        expected_shop_url = "https://jupiter.cloud.planittesting.com/#/shop"
        self.wait.until(EC.url_to_be(expected_shop_url))
        self.assertEqual(self.driver.current_url, expected_shop_url, "FAIL: Shop url is incorrect")
        print("PASS: Shop page URL validated.")
        time.sleep(5)

    def purchase_item(self, item_name, quantity, cart_count):
        # Find and print Teddy Bear price
        price = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='product-" + self.item[item_name]['item_code'] +"']/div/p/span"))).text
        print(f"INFO: Teddy Bear Price: {price}")
        self.item[item_name]['price'] = price

        # Click Buy button for Teddy Bear
        for _ in range(quantity):
            buy_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='product-" + self.item[item_name]['item_code'] +"']/div/p/a")))
            buy_button.click()
            print("EVENT: Teddy Bear added to cart.")

        # Check cart count is quantity
        cart_item = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='nav-cart']/a/span"))).text
        self.assertEqual(cart_item, str(cart_count), "FAIL: Cart count is incorrect")
        print(f"PASS: Cart count is {cart_count}.")
        time.sleep(5)

    def click_validate_cart_page(self):
        # Click Cart button
        cart_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav-cart']/a")))
        cart_button.click()
        print("EVENT: Navigated to Cart page.")

        # Validate Cart page URL
        expected_cart_url = "https://jupiter.cloud.planittesting.com/#/cart"
        self.wait.until(EC.url_to_be(expected_cart_url))
        self.assertEqual(self.driver.current_url, expected_cart_url, 'FAIL: cart URL is not matching')
        print("PASS: Cart page URL validated.")
        time.sleep(5)

    def validate_cart(self, shopping_list):
        # Find and print the number of rows in the cart table
        # cart_table = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/form/table")))
        # rows = cart_table.find_elements(By.TAG_NAME, "tr")
        # print(f"PASS: Number of rows in the cart table: {len(rows)}")

        calculated_total = 0

        # Extract and validate details from the cart table
        for index in range(1, len(shopping_list) + 1):
            name = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[" + str(index) + "]/td[1]"))).text
            price = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[" + str(index) + "]/td[2]"))).text
            subtotal = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[" + str(index) + "]/td[4]"))).text

            print(f"DATA: Item Details - Name: {name}, Price: {price}, Subtotal: {subtotal}")
            self.assertEqual(self.item[name]['price'], price, f"FAIL: Price : {self.item[name]['price']}  and ${price} are not matching.")
            print(f"PASS: Price of {name} is matched")

            actual_subtotal = float(subtotal.strip().replace('$',''))
            expected_subtotal = int(shopping_list[name]) * float(price.strip().replace('$',''))
            self.assertEqual(actual_subtotal, expected_subtotal, f'FAIL: Subtotal : {actual_subtotal}  and ${expected_subtotal} are  not matching.')
            print(f"PASS: Subtotal of {name} is matched")
            calculated_total += expected_subtotal

        # Extract and validate total amount
        total_price = (self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/form/table/tfoot/tr[1]/td/strong"))).text).split(':')[1].strip()
        print(f"PASS: Total Price in Cart: {total_price}")
        actual_total = float(total_price.strip().replace('$',''))
        self.assertEqual(actual_total, calculated_total, f'FAIL: Total : {actual_total}  and ${calculated_total} are not matching.')
        print(f"PASS: Total price is matched")
        time.sleep(5)

    def tearDown(self):
        """Close the browser."""
        self.driver.quit()
        print("PASS: Browser closed successfully.")

if __name__ == "__main__":
    unittest.main()
