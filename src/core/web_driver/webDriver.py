import undetected_chromedriver as uc
from selenium.webdriver.common.by import By 

class WebDriver: 
    def __init__(self):
        # Define a custom user agent
        my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        
        # Set up Chrome options
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f"user-agent={my_user_agent}")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-file-access-from-files")
        options.add_argument("--allow-file-access")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Initialize Chrome WebDriver with the specified options
        self.driver = uc.Chrome(options=options)

    def getPageContent(self, url_crawl, cmd, postData=None):
        url = f"http://localhost:3000/api/web-page?cmd={cmd}&path={url_crawl}"
        if postData:
            url = url + f'&postData={postData}'

        self.driver.get(url)

    
    def getElementByClass(self, className):
        return self.driver.find_elements(By.CLASS_NAME, className)
    
    def getElementByCssSelector(self, css_selector):
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)