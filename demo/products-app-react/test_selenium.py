from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Options to ignore SSL errors
options = Options()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to the products page
    driver.get('http://localhost:3000/products')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Test creating a product
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Create Product'))).click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'name')))

    driver.find_element(By.NAME, 'name').send_keys('Test Product')
    driver.find_element(By.NAME, 'description').send_keys('Test Description')
    driver.find_element(By.NAME, 'price').send_keys('100')
    driver.find_element(By.NAME, 'quantity').send_keys('10')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Test Product'))
    # Add wait for the product to be created
    time.sleep(5)

    # Test updating a product
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Edit'))).click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'name')))

    driver.find_element(By.NAME, 'name').clear()
    driver.find_element(By.NAME, 'name').send_keys('Updated Product')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Updated Product'))
    # Add wait for the product to be updated
    time.sleep(5)

    # Test deleting a product
    delete_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Delete']"))
    )
    delete_button.click()
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.LINK_TEXT, 'Updated Product')))
    # Add wait for the product to be deleted
    time.sleep(5)
finally:
    driver.quit()