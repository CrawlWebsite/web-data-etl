from core.web_driver.webDriver import WebDriver


class Website():
    def __init__(self, url):
        self.url = url
        self.webDriver = WebDriver()

    def getPageContent(self):
        self.webDriver.getPageContent(cmd='get', url_crawl=self.url)

    def excuteCrawl(self):
        pass

    def getElementByClass(self):
        pass