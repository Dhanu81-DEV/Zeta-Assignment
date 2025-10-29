
# Automation Script: Add to Cart → Checkout Flow

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from faker import Faker
import time

fake = Faker()
first_name = fake.first_name()
last_name = fake.last_name()
postal_code = fake.postcode()

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

try:
    # Step 1: go to url
    driver.get("https://www.saucedemo.com/")
    print("Opened saucedemo application...")

    # Step 2: Login with valid credentialss
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    print("Login successful...")

    # Step 3: Add product to cart
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    print("Product added to cart...")

    # Step 4: Proceed to checkout
    driver.find_element(By.ID, "checkout").click()

    # Step 5: Entering faker data
    driver.find_element(By.ID, "first-name").send_keys(first_name)
    driver.find_element(By.ID, "last-name").send_keys(last_name)
    driver.find_element(By.ID, "postal-code").send_keys(postal_code)
    driver.find_element(By.ID, "continue").click()
    print(f"Checkout details filled for {first_name} {last_name}, ZIP: {postal_code}")

    # Step 6: Complete purchase
    driver.find_element(By.ID, "finish").click()
    time.sleep(2)

    # Step 7: Validate successful order
    success_text = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "THANK YOU" in success_text.upper()
    print("Test Passed: Checkout flow completed successfully.")

except AssertionError:
    print("Test Failed: Checkout success message not found.")
except Exception as e:
    print(f"Test Failed due to unexpected error: {e}")
finally:
    driver.quit()
