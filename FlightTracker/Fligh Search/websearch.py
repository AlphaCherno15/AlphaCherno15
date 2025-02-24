from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.wayfair.ca/furniture/pdp/august-grove-adaija-18w-nightstand-with-charging-station-farmhouse-end-table-with-2-drawers-open-storage-c009722063.html?piid=2025445603")

# departure = driver.find_element(By.NAME, value='fName')
# departure.click()
# departure.send_keys("charlottetown")11

# driver.quit()