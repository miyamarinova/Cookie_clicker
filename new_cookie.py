from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

s = Service("/Users/miyamarinova/Development/chromedriver.exe")
o = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=s, options=o)

driver.get('https://orteil.dashnet.org/experiments/cookie/')

cookie = driver.find_element(By.ID, 'cookie')

items = driver.find_elements(By.CSS_SELECTOR, "#store div")
items_id = [item.get_attribute("id") for item in items]
items_id.remove('buyElder Pledge')

items_b = driver.find_elements(By.CSS_SELECTOR, "#store b")
items_text = [item.text for item in items_b]
items_text.remove('')
item_price = [item.split("-") for item in items_text]
prices = [int(price[1].replace(',', '')) for price in item_price]

time_seconds = time.time() + 5
timeout = time.time() + 60 * 5
element_index = 0

while True:
    cookie.click()
    buy_item = False
    money = int(driver.find_element(By.ID, 'money').text.replace(',', ''))

    if time.time() > time_seconds:

        for price in prices:
            if money > price:
                element_index = prices.index(price)
                buy_item = True

        if buy_item:
            new_item = driver.find_element(By.ID, items_id[element_index])
            new_item.click()
            buy_item = False

        time_seconds = time.time() + 5

    if time.time() > timeout:
        cookie_per_sec = driver.find_element(By.ID, "cps").text
        print(cookie_per_sec)
        break

driver.quit()