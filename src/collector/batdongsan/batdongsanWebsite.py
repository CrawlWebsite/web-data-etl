from core.web_driver.webDriver import WebDriver
from core.website.website import Website

class BatDongSanWebsite(Website):
    def __init__(self, url):
        super().__init__(url)

class BatDongSanWebsiteFactory:
    def create(url):
        return BatDongSanWebsite(url)
   