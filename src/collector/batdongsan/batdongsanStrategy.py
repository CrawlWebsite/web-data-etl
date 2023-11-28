import re
from core.web_driver.webDriver import WebDriver
from entity.apartment import ApartmentAddress
from entity.sale import Sale
from selenium.webdriver.common.by import By 
from core.real_estate.realEstateStrategy import RealEstateStrategy
from collector.batdongsan.batdongsanWebsite import BatDongSanWebsite, BatDongSanWebsiteFactory


class BatDongSanStrategy(RealEstateStrategy):
    website: BatDongSanWebsite
    sale: Sale

    def __init__(self, url):
        self.website = BatDongSanWebsiteFactory.create(url)
      
        self.phoneDecryptDriver = WebDriver()
        self.phoneDecryptUrl = 'https://batdongsan.com.vn/Product/ProductDetail/DecryptPhone'

        self.sale = Sale()
        self.apartmentAddress = ApartmentAddress()

    def changeWebsite(self, url):
        self.website.changeUrl(url)

    def crawlSale(self):
        self.crawlName()
        self.crawlPhoneNumber()

    def crawlApartmentAddress(self):
        addressElements = self.website.getElementByCssSelector(css_selector='div.js__breadcrumb a')

        for addressElement in addressElements:
            level = addressElement.get_attribute('level')
            value = addressElement.get_attribute('innerHTML')

            self.updateApartmentAddressByLevel(level, value)
    

    def crawlApartmentInfo(self):
        infoElements = self.website.getElementByCssSelector(css_selector='div.re__pr-specs-content-item')
        
        for infoElement in infoElements:
            infoSpans = infoElement.find_elements(By.CSS_SELECTOR, 'span')[0]
            print(infoSpans.get_attributes('class'))


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
        self.phoneDecryptDriver.getPageContent(cmd='post', url_crawl=self.phoneDecryptUrl, postData=f'PhoneNumber={phoneRaw}')

        # Get phone
        phoneNumber = self.phoneDecryptDriver.getElementByCssSelector(css_selector='pre')[0].get_attribute('innerHTML')
        phoneNumber = re.sub(r'\s', '', phoneNumber)

        self.sale.setPhoneNumber(phoneNumber)

    def updateApartmentAddressByLevel(self, level, value):
        match level:
            case "2":
                self.apartmentAddress.setCity(value)
            case "3":
                self.apartmentAddress.setDistrict(value)

    def excuteCrawl(self):
        self.crawlSale()
        self.crawlApartmentInfo()
        self.crawlApartmentAddress()