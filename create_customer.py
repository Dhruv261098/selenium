from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import random


# Odoo login credentials
ODOO_URL = "http://34.125.145.208:8077/web/login"
CUSTOMER_URL = "http://34.125.145.208:8077/odoo/sale-customers/new"
USERNAME = "dhruv.desai.2610@gmail.com"
PASSWORD = "selenium@2025"


# Logging setup
logging.basicConfig(
    filename="customer_creation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Chrome WebDriver options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no UI)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start WebDriver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

try:
    # Step 1: Login
    logging.info("Opening Odoo login page...")
    driver.get(ODOO_URL)
    time.sleep(2)  # Give some time for the page to load

    # Scroll down to make sure all elements are visible
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for Email field to be visible & interactable
    logging.info("Waiting for email input field...")
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='login']"))
    )
    driver.execute_script("arguments[0].click();", email_input)
    email_input.send_keys(USERNAME)

    # Wait for Password field
    logging.info("Waiting for password input field...")
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
    )
    driver.execute_script("arguments[0].click();", password_input)
    password_input.send_keys(PASSWORD)

    # Wait for the "Log in" button
    logging.info("Waiting for login button...")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Log in')]"))
    )

    # Scroll into view before clicking
    driver.execute_script("arguments[0].scrollIntoView();", login_button)
    time.sleep(1)  # Small delay to ensure visibility

    # Screenshot before clicking login
    driver.save_screenshot("before_click_login.png")

    # Click login button
    logging.info("Clicking login button...")
    driver.execute_script("arguments[0].click();", login_button)

    # Wait for a possible login error message
    try:
        error_message = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger"))
        ).text
        logging.error(f"❌ Login Failed! Odoo Error: {error_message}")
        print(f"❌ Login Failed! Odoo Error: {error_message}")
        driver.quit()
        exit()
    except:
        logging.info("No login error message detected.")

    # Screenshot after login attempt
    driver.save_screenshot("after_login_attempt.png")

    # Check the current URL to verify login success
    current_url = driver.current_url
    logging.info(f"Current URL after login: {current_url}")
    print("Current URL after login:", current_url)

    # ✅ Check if login was successful
    if any(keyword in current_url for keyword in ["/web", "/odoo"]) and "login" not in current_url:
        logging.info("✅ Login Successful!")
        print("✅ Login Successful!")
    else:
        logging.error("❌ Login Failed!")
        print("❌ Login Failed!")
        driver.quit()
        exit()

    # Step 2: Navigate Directly to New Customer Page
    logging.info(f"Navigating directly to: {CUSTOMER_URL}")
    driver.get(CUSTOMER_URL)

    # Wait for page load & verify we are on the New Customer Page
    time.sleep(3)  # Allow page to load
    current_url = driver.current_url
    logging.info(f"Current URL after navigation: {current_url}")
    print(f"Current URL after navigation: {current_url}")

    # ✅ Take a screenshot after navigating to the new customer page
    driver.save_screenshot("after_navigating_to_customer.png")

    if "/sale-customers/new" in current_url:
        logging.info("✅ Successfully reached the New Customer form.")
    else:
        logging.error("❌ Failed to open the New Customer form!")
        driver.save_screenshot("error_new_page.png")  # Save screenshot for debugging
        driver.quit()
        exit()


    # Step 3: Select "Individual" Option
    try:
        logging.info("Selecting 'Individual' customer type...")
        individual_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Individual')]/preceding-sibling::input"))
        )
        driver.execute_script("arguments[0].click();", individual_radio)

        # Take a screenshot after selecting Individual
        driver.save_screenshot("after_selecting_individual.png")
        logging.info("✅ Selected 'Individual' successfully!")

    except Exception as e:
        logging.error(f"❌ Failed to select 'Individual': {str(e)}")
        driver.save_screenshot("error_selecting_individual.png")
        driver.quit()
        exit()



    # Step 4: Fill Name Field with a Random North American Name


    # Random North American Names
    NORTH_AMERICA_NAMES = [
        "James Smith", "Emma Johnson", "Oliver Williams", "Charlotte Brown",
        "Liam Jones", "Sophia Garcia", "Benjamin Miller", "Isabella Martinez"
    ]
    RANDOM_NAME = random.choice(NORTH_AMERICA_NAMES)

    # Wait for placeholder to be "e.g. Brandon Freeman"
    name_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='e.g. Brandon Freeman']"))
    )
    logging.info("✅ Found name field with placeholder 'e.g. Brandon Freeman'")
    
    # Click to activate the field (move cursor there)
    driver.execute_script("arguments[0].scrollIntoView();", name_input)
    driver.execute_script("arguments[0].click();", name_input)
    time.sleep(1)
    driver.save_screenshot("step_1_clicked_placeholder.png")
    logging.info("📸 Screenshot after clicking name placeholder taken")
    
    # Remove any protection & fill name
    driver.execute_script("arguments[0].removeAttribute('readonly');", name_input)
    driver.execute_script("arguments[0].removeAttribute('disabled');", name_input)
    time.sleep(1)
    
    name_input.send_keys(RANDOM_NAME)
    time.sleep(1)
    name_input.send_keys(Keys.TAB)
    logging.info(f"✅ Name '{RANDOM_NAME}' entered into the name field")
    
    # Screenshot after filling name
    driver.save_screenshot("step_2_after_filling_name.png")
    logging.info("📸 Screenshot after filling name taken")


    
    # Step 5: Select Country (Typing + Enter to select)
    try:
        COUNTRY_LIST = ["India", "Canada", "Singapore", "Belgium", "Brazil", "Australia"]
        RANDOM_COUNTRY = random.choice(COUNTRY_LIST)
    
        logging.info(f"Typing and selecting '{RANDOM_COUNTRY}' in the Country field...")
    
        # Click the dropdown to activate input
        country_field_div = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@name, 'country_id')]"))
        )
        country_field_div.click()
        time.sleep(1)
    
        # Target the actual input field
        country_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@name, 'country_id')]//input"))
        )
    
        # Type country name
        country_input.clear()
        country_input.send_keys(RANDOM_COUNTRY)
        time.sleep(1)
    
        # Screenshot after typing
        driver.save_screenshot(f"step_country_typed_{RANDOM_COUNTRY}.png")
        logging.info(f"📸 Screenshot taken after typing country: {RANDOM_COUNTRY}")
    
        # Press Enter to confirm selection
        country_input.send_keys(Keys.ENTER)
        time.sleep(1.5)  # Give it time to apply selection
    
        # Screenshot after pressing enter (should be selected)
        driver.save_screenshot(f"step_country_selected_{RANDOM_COUNTRY}.png")
        logging.info(f"✅ Country '{RANDOM_COUNTRY}' selected with Enter key.")
    
    except Exception as e:
        logging.error(f"❌ Failed to select country '{RANDOM_COUNTRY}': {str(e)}")
        driver.save_screenshot("error_country_selection.png")
        driver.quit()
        exit()

    # Step 6: Enter City
    try:
        logging.info("Typing city name 'Patan'...")
    
        city_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='City']"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", city_input)
        time.sleep(1)
        city_input.clear()
        city_input.send_keys("Patan")
        time.sleep(1)
    
        # Screenshot after typing city
        driver.save_screenshot("step_city_entered_patan.png")
        logging.info("📸 Screenshot taken after entering city 'Patan'")
    
    except Exception as e:
        logging.error(f"❌ Failed to enter city: {str(e)}")
        driver.save_screenshot("error_city_input.png")
        driver.quit()
        exit()
    
except Exception as e:
    logging.error(f"⚠️ Error: {str(e)}")
    print(f"⚠️ Error: {str(e)}")

finally:
    driver.quit()

