import requests
import undetected_chromedriver as uc
import time 
import re
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date

# Define a custom user agent
my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
 
# Set up Chrome options
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument(f"user-agent={my_user_agent}")
 
# Initialize Chrome WebDriver with the specified options
driver = uc.Chrome(options=options)
 
today = date.today()

url_crawl = "https://batdongsan.com.vn/ban-can-ho-chung-cu-goldsilk-complex"
driver.get(f"http://localhost:3000/?cmd=get&path={url_crawl}")
time.sleep(5)

elements = driver.find_elements(By.CLASS_NAME, "js__product-link-for-product-id")

# Get list element in page
lst = [element.get_attribute("href") for element in elements]

# Sale list
sales = []

for url in lst:
    try: 
        url_new = url.replace('http://localhost:3000','http://localhost:3000/?cmd=get&path=https://batdongsan.com.vn')
        driver.get(url_new)

        # Get name
        nameElement = driver.find_elements(By.CSS_SELECTOR, "div.re__contact-name.js_contact-name")[0]
        name = nameElement.get_attribute('title')
        
        # Get phone raw
        phoneElement = driver.find_elements(By.CSS_SELECTOR, 'div.phone.js__phone')[0]
        phone_raw = phoneElement.get_attribute('raw')

        # Call API to decrypt phone raw
        url_crawl_phone = "https://batdongsan.com.vn/Product/ProductDetail/DecryptPhone"
        driver.get(f"http://localhost:3000/?path={url_crawl_phone}&postData=PhoneNumber={phone_raw}&cmd=post")

        # Get phone
        phone_number = driver.find_elements(By.CSS_SELECTOR, 'pre')[0].get_attribute('innerHTML')
        phone_number = re.sub(r'\s', '', phone_number)

        sales.append({
            'name': name, 
            'phone': phone_number
        })

        print("Crawl success: " + url_new)
    except Exception as ex:
        print("Crawl failure: " + url_new)
        print(ex)


# Insert sale data to database
requests.post(f"http://localhost:3000/user/bulk", json={'users': sales})

driver.close()
