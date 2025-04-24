from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@given("the user navigates to the Shop page")
def step_navigate_to_shop_page(context):
    context.driver = webdriver.Chrome()
    context.driver.set_window_size(1920, 1080)
    context.driver.implicitly_wait(10)
    context.driver.get("https://jupiter.cloud.planittesting.com")
    shop_link = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav-shop']/a")))
    shop_link.click()

@when("the user purchases the following items")
def step_purchase_items(context):
    context.cart_count = 0
    context.shopping_type = 0
    context.item_dict = {'Teddy Bear': {'item_code': '1', 'price': ''}, 'Stuffed Frog': {'item_code': '2', 'price': ''},
                 'Handmade Doll': {'item_code': '3', 'price': ''}, 'Fluffy Bunny': {'item_code': '4', 'price': ''},
                 'Smiley Bear': {'item_code': '5', 'price': ''}, 'Funny Cow': {'item_code': '6', 'price': ''},
                 'Valentine Bear': {'item_code': '7', 'price': ''}, 'Smiley Face': {'item_code': '8', 'price': ''}
                 }
    for row in context.table:
        item_name = row["Item"]
        quantity = int(row["Quantity"])
        price = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='product-" + context.item_dict[item_name]['item_code'] + "']/div/p/span"))).text
        context.item_dict[item_name]['price'] = price
        context.item_dict[item_name]['quantity'] = quantity
        for _ in range(quantity):
            buy_button = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='product-" + context.item_dict[item_name]['item_code'] +"']/div/p/a")))
            buy_button.click()
        context.cart_count += quantity
        context.shopping_type += 1
    time.sleep(5)

@then("the cart count should be correct")
def step_validate_cart_count(context):
    print(context.item_dict)
    cart_item = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='nav-cart']/a/span"))).text
    time.sleep(5)
    assert int(cart_item) == context.cart_count

@then("the user navigates to the Cart page")
def step_navigate_to_cart(context):
    cart_button = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav-cart']/a")))
    cart_button.click()

@then("the cart items should match their expected subtotal and total")
def step_validate_cart(context):
    calculated_total = 0

    # Extract and validate details from the cart table
    for index in range(1, context.shopping_type + 1):
        name = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[" + str(index) + "]/td[1]"))).text
        price = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[" + str(index) + "]/td[2]"))).text
        subtotal = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/form/table/tbody/tr[" + str(index) + "]/td[4]"))).text

        print(f"DATA: Item Details - Name: {name}, Price: {price}, Subtotal: {subtotal}")
        assert context.item_dict[name]['price'] == price

        actual_subtotal = float(subtotal.strip().replace('$', ''))
        expected_subtotal = int(context.item_dict[name]['quantity']) * float(price.strip().replace('$', ''))
        assert actual_subtotal == expected_subtotal
        calculated_total += expected_subtotal

    # Extract and validate total amount
    total_price = (WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/form/table/tfoot/tr[1]/td/strong"))).text).split(':')[1].strip()
    actual_total = float(total_price.strip().replace('$', ''))
    assert actual_total == calculated_total
    time.sleep(5)

    context.driver.quit()
