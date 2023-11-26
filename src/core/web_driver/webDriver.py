import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

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

    def getPageContent(self, url_crawl, cmd):
        self.driver.get(f"http://localhost:3000/api/web-page?cmd={cmd}&path={url_crawl}")