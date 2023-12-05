import re
from config.logger import LoggerCustom
from selenium.webdriver.common.by import By 

from core.web_driver.webDriver import WebDriver
from core.real_estate.realEstateStrategy import RealEstateStrategy

from entity.apartment import ApartmentAddress, ApartmentInfo
from entity.sale import Sale

from collector.batdongsan.batdongsanWebsite import BatDongSanWebsite, BatDongSanWebsiteFactory


class BatDongSanStrategy(RealEstateStrategy):
    website: BatDongSanWebsite
    sale: Sale

    def __init__(self, url):
        self.logger = LoggerCustom(BatDongSanStrategy.__name__)
        self.website = BatDongSanWebsiteFactory.create(url)
      
        self.phoneDecryptDriver = WebDriver()
        self.phoneDecryptUrl = 'https://batdongsan.com.vn/Product/ProductDetail/DecryptPhone'

        self.sale = Sale()
        self.apartmentAddress = ApartmentAddress()
        self.apartmentInfo = ApartmentInfo()

    def changeWebsite(self, url):
        self.website.changeUrl(url)

    def crawlSale(self):
        self.logger.info("Crawling sale ...")

        self.crawlName()
        self.crawlPhoneNumber()

        self.logger.info("Crawling sale successfully")

    def crawlApartmentAddress(self):
        self.logger.info("Crawling address ...")

        addressElements = self.website.getElementByCssSelector(css_selector='div.js__breadcrumb a')

        # Crawl city and district
        for addressElement in addressElements:
            level = addressElement.get_attribute('level')
            value = addressElement.get_attribute('innerHTML')

            self.updateApartmentAddressByLevel(level, value)
    
        # Crawl project
        projectElement = self.website.getElementByCssSelector(css_selector='div.re__project-title')[0]
        project = projectElement.get_attribute('innerHTML')
        self.apartmentAddress.setProject(project)

        # Crawl address
        addressElement = self.website.getElementByCssSelector(css_selector='span.js__pr-address')[0]
        address = addressElement.get_attribute('innerHTML')
        self.apartmentAddress.setAddress(address)

        self.logger.info("Crawling address successfully")


    def crawlApartmentInfo(self):
        self.logger.info("Crawling information ...")

        infoElements = self.website.getElementByCssSelector(css_selector='div.re__pr-specs-content-item')
        
        for infoElement in infoElements:
            iconElement = infoElement.find_elements(By.CSS_SELECTOR, 'span i')[0]
            iconClass = iconElement.get_attribute('class')

            valueElement = infoElement.find_elements(By.CSS_SELECTOR, 'span.re__pr-specs-content-item-value')[0]
            value = valueElement.get_attribute('innerHTML')

            self.updateApartmentInfoByIconClass(iconClass, value)

        self.logger.info("Crawling information successfully")


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

    def updateApartmentInfoByIconClass(self, iconClass, value):
        match iconClass:
            case "re__icon-size":
                self.apartmentInfo.setAcreage(value)
            case "re__icon-front-view":
                self.apartmentInfo.setBalconyDirection(value)
            case "re__icon-private-house":
                self.apartmentInfo.setApartmentDirection(value)
            case "re__icon-bedroom":
                self.apartmentInfo.setNumberOfBedRoom(value)
            case "re__icon-bath":
                self.apartmentInfo.setNumberOfToilet(value)
            case "re__icon-document":
                self.apartmentInfo.setJuridical(value)
            case "re__icon-interior": 
                self.apartmentInfo.setInterior(value)
            case "re__icon-apartment":
                self.apartmentInfo.setNumberOfFloor(value)

    def excuteCrawl(self):
        try:
            self.crawlSale()
            self.crawlApartmentInfo()
            self.crawlApartmentAddress()
        except Exception as ex:
            print("Exception: ", ex)