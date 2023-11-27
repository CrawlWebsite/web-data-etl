import re
from entity.sale import Sale
from selenium.webdriver.common.by import By 
from core.real_estate.realEstateStrategy import RealEstateStrategy
from collector.batdongsan.batdongsanWebsite import BatDongSanWebsite, BatDongSanWebsiteFactory


class BatDongSanStrategy(RealEstateStrategy):
    website: BatDongSanWebsite
    sale: Sale

    def __init__(self, url):
        self.website = BatDongSanWebsiteFactory.create(url)
        self.sale = Sale()
   
    def changeWebsite(self, url):
        self.website.changeUrl(url)

    def crawlName(self):
        nameElement = self.website.getElementByCssSelector("div.re__contact-name.js_contact-name")

        name = ''
        if nameElement and nameElement[0]:
            name = nameElement[0].get_attribute('title')

        self.sale.setName(name)


    def crawlPhoneNumber(self):
        # Get phone raw
        phoneElement = self.website.getElementByCssSelector("div.phone.js__phone")

        if not (phoneElement and phoneElement[0]):
            return ''
        
        phoneRaw = phoneElement[0].get_attribute('raw')
        print(phoneRaw)

        # Call API to decrypt phone raw
        url_crawl = 'https://batdongsan.com.vn/Product/ProductDetail/DecryptPhone'
        self.website.phoneDecryptDriver.getPageContent(cmd='post', url_crawl=url_crawl, postData=f'PhoneNumber={phoneRaw}')

        # Get phone
        phoneNumber = self.website.phoneDecryptDriver.getElementByCssSelector(css_selector='pre')[0].get_attribute('innerHTML')
        phoneNumber = re.sub(r'\s', '', phoneNumber)

        self.sale.setPhoneNumber(phoneNumber)

    def excuteCrawl(self):
        self.crawlName()
        self.crawlPhoneNumber()