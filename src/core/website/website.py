from selenium.webdriver.common.by import By 
from core.web_driver.webDriver import WebDriver


class Website():
    def __init__(self, url):
        self.url = url
        self.webDriver = WebDriver()
        self.getPageContent()

    def changeUrl(self, url):
        self.url = url
        self.webDriver.getPageContent(cmd='get', url_crawl=url)

    def getPageContent(self):
        self.webDriver.getPageContent(cmd='get', url_crawl=self.url)

    def getElementByClass(self, className):
        return self.webDriver.getElementByClass(className=className)
    
    def getElementByCssSelector(self, css_selector):
        return self.webDriver.getElementByCssSelector(css_selector=css_selector)