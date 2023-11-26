from core.web_driver.webDriver import WebDriver
from core.website.website import Website
import re

class BatDongSanWebsite(Website):
    def __init__(self, url):
        super().__init__(url)
        self.phoneDecryptDriver = WebDriver()


    def crawlName(self):
        nameElement = self.getElementByCssSelector("div.re__contact-name.js_contact-name")

        if nameElement and nameElement[0]:
            return nameElement[0].get_attribute('title')

        return ''

    def crawlPhoneNumber(self):
        # Get phone raw
        phoneElement = self.getElementByCssSelector("div.phone.js__phone")

        if not (phoneElement and phoneElement[0]):
            return ''
        
        phoneRaw = phoneElement[0].get_attribute('raw')
        print(phoneRaw)

        # Call API to decrypt phone raw
        url_crawl = 'https://batdongsan.com.vn/Product/ProductDetail/DecryptPhone'
        self.phoneDecryptDriver.getPageContent(cmd='post', url_crawl=url_crawl, postData=f'PhoneNumber={phoneRaw}')

        # Get phone
        phoneNumber = self.phoneDecryptDriver.getElementByCssSelector(css_selector='pre')[0].get_attribute('innerHTML')
        phoneNumber = re.sub(r'\s', '', phoneNumber)

        return phoneNumber

    def excuteCrawl(self):
        self.crawlName()
        self.crawlPhoneNumber()


class BatDongSanWebsiteFactory(Website):
    def create(url):
        return BatDongSanWebsite(url)
   