from selenium.webdriver.common.by import By 
from core.web_driver.webDriver import WebDriver


class Website():
    def __init__(self, url):
        self.url = url
        self.webDriver = WebDriver()
        self.getPageContent()

    def getPageContent(self):
        print(222)
        self.webDriver.getPageContent(cmd='get', url_crawl=self.url)

    def getElementByClass(self, className):
        print("111",className)
        return self.webDriver.driver.find_elements(By.CLASS_NAME, className)
    
    def getElementByCssSelector(self, css_selector):
        print("css_selector",css_selector)
        f = open("demofile2.html", "a")
        f.write(self.webDriver.driver.page_source)
        f.close()
        return self.webDriver.driver.find_elements(By.CSS_SELECTOR, css_selector)