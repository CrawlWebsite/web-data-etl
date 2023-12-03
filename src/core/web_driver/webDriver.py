import undetected_chromedriver as uc
from selenium.webdriver.common.by import By 
import time 

class WebDriver: 
    def __init__(self):
        options = uc.ChromeOptions()

        # Set options to make the ChromeDriver less detectable
        options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--blink-settings=imagesEnabled=false')  # Disable loading of images
        options.add_argument('--enable-blink-features=DisableJavaScript')  # Disable JavaScript execution

        # Initialize Chrome WebDriver with the specified options
        self.driver = uc.Chrome(options=options)

    def getPageContent(self, url_crawl, cmd, postData=None):
        url = f"http://localhost:3000/api/web-page?cmd={cmd}&path={url_crawl}"
        if postData:
            url = url + f'&postData={postData}'

        self.driver.get(url)
        time.sleep(2)
        print(f"Get page {url_crawl} successful")

    
    def getElementByClass(self, className):
        return self.driver.find_elements(By.CLASS_NAME, className)
    
    def getElementByCssSelector(self, css_selector):
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)