import undetected_chromedriver as uc

class WebDriver: 
    def __init__(self):
        # Define a custom user agent
        my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        
        # Set up Chrome options
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f"user-agent={my_user_agent}")
        
        # Initialize Chrome WebDriver with the specified options
        self.driver = uc.Chrome(options=options)

    def getPageContent(self, url_crawl, cmd):
        self.driver.get(f"http://localhost:3000/?cmd={cmd}&path={url_crawl}")