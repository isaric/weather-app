from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Create directory for screenshots if it doesn't exist
os.makedirs("doc", exist_ok=True)

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")

# Initialize the driver
driver = webdriver.Chrome(options=options)


try:
    # Screenshot 1: Start Page
    print("Taking screenshot of the start page...")
    driver.get("http://localhost:5000")
    time.sleep(2)  # Wait for page to fully load

    def get_scroll_dimension(axis):
        return driver.execute_script(f"return document.body.parentNode.scroll{axis}")

    width = get_scroll_dimension("Width")
    height = get_scroll_dimension("Height") * 1.3
    driver.set_window_size(width, height)
    full_body_element = driver.find_element(By.TAG_NAME, "body")
    full_body_element.screenshot("doc/screen_1.png")
    print("Start page screenshot saved.")

    # Screenshot 2: City Search with Autocomplete
    print("Taking screenshot of city search with autocomplete...")
    search_box = driver.find_element(By.ID, "city")
    search_box.clear()
    search_box.send_keys("Zagreb")
    time.sleep(2)  # Wait for autocomplete results
    width = get_scroll_dimension("Width")
    height = get_scroll_dimension("Height") * 1.3
    driver.set_window_size(width, height)
    full_body_element = driver.find_element(By.TAG_NAME, "body")
    full_body_element.screenshot("doc/screen_2.png")
    print("City search screenshot saved.")

    # Select a city from autocomplete for the next screenshots
    city_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cityList"))
    )
    city_options = city_list.find_elements(By.TAG_NAME, "li")
    if city_options:
        city_options[0].click()
    else:
        print("No city options found. Using 'New York' as fallback.")
        search_box.clear()
        search_box.send_keys("New York, US (40.7128,-74.006)")

    # Screenshot 3: Prognosis Report
    print("Taking screenshot of prognosis report...")
    # Select "Forecast" radio button
    forecast_radio = driver.find_element(By.ID, "report1")
    forecast_radio.click()
    
    # Click submit button
    submit_button = driver.find_element(By.ID, "main-button")
    submit_button.click()
    
    # Wait for report page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "map"))
    )
    time.sleep(3)  # Wait for map and plot to fully render
    width = get_scroll_dimension("Width")
    height = get_scroll_dimension("Height") * 1.3
    driver.set_window_size(width, height)
    full_body_element = driver.find_element(By.TAG_NAME, "body")
    full_body_element.screenshot("doc/screen_3.png")
    print("Prognosis report screenshot saved.")

    print("Go back to home page")
    back_button = driver.find_element(By.CLASS_NAME, "back-button")
    actions = ActionChains(driver)
    actions.move_to_element(back_button).perform()
    back_button.click()

    print("Wait for home page to load")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "city"))
    )
    
    print("Re-enter city")
    search_box = driver.find_element(By.ID, "city")
    search_box.clear()
    search_box.send_keys("Zagreb")
    time.sleep(2)
    city_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cityList"))
    )
    city_options = city_list.find_elements(By.TAG_NAME, "li")
    if city_options:
        city_options[0].click()
    
    # Screenshot 4: Historical Report
    print("Taking screenshot of historical report...")
    # Select "10-day History" radio button
    historical_radio = driver.find_element(By.ID, "report2")
    historical_radio.click()
    
    # Click submit button
    submit_button = driver.find_element(By.ID, "main-button")
    submit_button.click()
    
    # Wait for report page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "map"))
    )
    time.sleep(3)  # Wait for map and plot to fully render
    width = get_scroll_dimension("Width")
    height = get_scroll_dimension("Height") * 1.3
    driver.set_window_size(width, height)
    full_body_element = driver.find_element(By.TAG_NAME, "body")
    full_body_element.screenshot("doc/screen_4.png")
    print("Historical report screenshot saved.")

    print("All screenshots have been taken successfully!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()


