from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")

driver = webdriver.Chrome(executable_path='/Users/flatironschool/Desktop/chromedriver', chrome_options=option)

driver.get("http://www.google.com")

print(driver.title)

inputElement = driver.find_element_by_name("q")

inputElement.send_keys("cheese!")

inputElement.submit()

try:
    WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))
    print(driver.title)

finally:
    driver.quit()
