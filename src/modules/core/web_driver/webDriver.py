from time import sleep
from selenium.webdriver.common.by import By 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config.envVar import API_HOST
from config.logger import LoggerCustom 

class WebDriver: 
    def __init__(self):
        options = webdriver.ChromeOptions()

        # Set options to make the ChromeDriver less detectable
        options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--blink-settings=imagesEnabled=false')  # Disable loading of images
        options.add_argument('--enable-blink-features=DisableJavaScript')  # Disable JavaScript execution

        # Initialize Chrome WebDriver with the specified options
        self.driver = webdriver.Chrome(options=options)
        self.logger = LoggerCustom(WebDriver.__name__)


    def getPageContent(self, url_crawl, cmd, postData=None):
        try:
            url = f"{API_HOST}/api/web-page?cmd={cmd}&path={url_crawl}"
            if postData:
                url = url + f'&postData={postData}'

            self.driver.get(url)
            self.driver.maximize_window()
            self.logger.info(f"Get page {url_crawl} successful")
        except Exception as ex:
            print(ex)
            sleep(10)
            self.driver.get(url)


    
    def getElementByClass(self, className):
        return self.driver.find_elements(By.CLASS_NAME, className)
    
    def getElementByCssSelector(self, css_selector):
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)
