import re
from config.logger import LoggerCustom
from selenium.webdriver.common.by import By 

from modules.core.web_driver.webDriver import WebDriver
from modules.core.real_estate.realEstateStrategy import RealEstateStrategy

from modules.entity.apartment import ApartmentAddress, ApartmentInfo
from modules.entity.apartmentSale import ApartmentSale
from modules.entity.sale import Sale

from modules.collector.batdongsan.batdongsanWebsite import BatDongSanSearchPageWebsite, BatDongSanSearchPageWebsiteFactory, BatDongSanWebsite, BatDongSanWebsiteFactory
from utils.numberFormat import stringToNumber


class BatDongSanStrategy(RealEstateStrategy):
    website: BatDongSanWebsite
    sale: Sale

    def __init__(self, url):
        self.logger = LoggerCustom(BatDongSanStrategy.__name__)
        self.website = BatDongSanWebsiteFactory.create(url)
        self.url = url
      
        self.phoneDecryptDriver = WebDriver()
        self.phoneDecryptUrl = 'https://batdongsan.com.vn/Product/ProductDetail/DecryptPhone'

        self.sale = Sale()
        self.apartmentAddress = ApartmentAddress()
        self.apartmentInfo = ApartmentInfo()
        self.apartmentSale = ApartmentSale()

    def changeWebsite(self, url):
        self.website.changeUrl(url)

    def crawlSale(self):
        try:
            self.logger.info("Crawling sale ...")

            self.crawlName()
            self.crawlPhoneNumber()

            self.logger.info(f"Crawling sale successfully: {self.sale.__dict__}")
        except Exception as ex:
            print(ex)

    def crawlApartmentAddress(self):
        try:
            self.logger.info("Crawling apartment address ...")

            addressElements = self.website.getElementByCssSelector(css_selector='div.js__breadcrumb a')

            # Crawl city and district
            for addressElement in addressElements:
                level = addressElement.get_attribute('level')
                value = addressElement.get_attribute('innerHTML')

                self.updateApartmentAddressByLevel(level, value)
        
            # Crawl project
            projectElement = self.website.getElementByCssSelector(css_selector='div.re__project-title')
            if len(projectElement) > 0:
                project = projectElement[0].get_attribute('innerHTML')
                self.apartmentAddress.setProject(project)

            # Crawl address
            addressElement = self.website.getElementByCssSelector(css_selector='span.js__pr-address')
            if len(addressElement) > 0:
                address = addressElement[0].get_attribute('innerHTML')
                self.apartmentAddress.setAddress(address)

            self.logger.info(f"Crawling apartment address successfully: {self.apartmentAddress.__dict__}")
        except Exception as ex:
            print(ex)

    def crawlApartmentInfo(self):
        try:
            self.logger.info("Crawling apartment information ...")

            infoElements = self.website.getElementByCssSelector(css_selector='div.re__pr-specs-content-item')
            
            for infoElement in infoElements:
                iconElement = infoElement.find_elements(By.CSS_SELECTOR, 'span i')
                if len(iconElement) > 0:
                    iconClass = iconElement[0].get_attribute('class')
                else:
                    iconClass = ''

                valueElement = infoElement.find_elements(By.CSS_SELECTOR, 'span.re__pr-specs-content-item-value')
                if len(valueElement) > 0:
                    value = valueElement[0].get_attribute('innerHTML')
                else: 
                    value = None
                self.updateApartmentInfoByIconClass(iconClass, value)

            # Crawl price
            priceWrapElement = self.website.getElementByCssSelector(css_selector='div.re__pr-short-info-item.js__pr-short-info-item')
            if len(priceWrapElement) > 0:
                priceValueElements = priceWrapElement[0].find_elements(By.CSS_SELECTOR, 'span')
            else:
                priceValueElements = None

            if len(priceValueElements) == 3:
                for priceValueElement in priceValueElements:
                    if priceValueElement.get_attribute('class') == 'value':
                        value = priceValueElement.get_attribute("innerHTML")
                        price, priceUnit = value.split(' ')
                        print(price, priceUnit)
                        self.apartmentInfo.setPrice(stringToNumber(price))
                        self.apartmentInfo.setPriceUnit(priceUnit)

                    if priceValueElement.get_attribute('class') == 'ext':
                        value = priceValueElement.get_attribute("innerHTML")
                        pricePerSquareMeter, pricePerSquareMeterUnit = value.split(' ')
                        print(pricePerSquareMeter[1:])
                       
                        self.apartmentInfo.setPricePerSquareMeter(stringToNumber(pricePerSquareMeter[1:]))
                        self.apartmentInfo.setPricePerSquareMeterUnit(pricePerSquareMeterUnit)

            
            self.logger.info(f"Crawling apartment information successfully: {self.apartmentInfo.__dict__}")
        except Exception as ex:
            print(ex)

    def crawlName(self):
        nameElement = self.website.getElementByCssSelector("div.re__contact-name.js_contact-name")

        if len(nameElement) > 0:
            name = nameElement[0].get_attribute('title')
            self.sale.setName(name)


    def crawlPhoneNumber(self):
        # Get phone raw
        phoneElement = self.website.getElementByCssSelector("div.phone.js__phone")

        if len(phoneElement) == 0:
            return ''
        
        phoneRaw = phoneElement[0].get_attribute('raw')

        # Call API to decrypt phone raw
        self.phoneDecryptDriver.getPageContent(cmd='post', url_crawl=self.phoneDecryptUrl, postData=f'PhoneNumber={phoneRaw}')

        # Get phone
        phoneNumberElement = self.phoneDecryptDriver.getElementByCssSelector(css_selector='pre')
        if len(phoneNumberElement) > 0:
            phoneNumber = re.sub(r'\s', '', phoneNumberElement[0].get_attribute('innerHTML'))
        else:
            phoneNumber = None
            
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
                acreage, acreageUnit = value.split(" ") if value is not None else [None, None]

                self.apartmentInfo.setAcreage(stringToNumber(acreage))
                self.apartmentInfo.setAcreageUnit(acreageUnit)

            case "re__icon-front-view":
                self.apartmentInfo.setBalconyDirection(value)
            case "re__icon-private-house":
                self.apartmentInfo.setApartmentDirection(value)
            case "re__icon-bedroom":
                self.apartmentInfo.setNumberOfBedRoom(value)
            case "re__icon-bath":
                self.apartmentInfo.setNumberOfToilet(value)
            case "re__icon-document":
                self.apartmentInfo.setLegal(value)
            case "re__icon-interior": 
                self.apartmentInfo.setInterior(value)
            case "re__icon-apartment":
                self.apartmentInfo.setNumberOfFloor(value)

    def crawlApartmentSale(self):
        try:
            self.logger.info("Crawling apartment sale ...")

            self.apartmentSale.setUrl(self.url)

            startDateElement, endDateElement = self.website.getElementByCssSelector("div.re__pr-short-info-item.js__pr-config-item span.value")[:2]

            self.apartmentSale.setStartDate(startDateElement.get_attribute('innerHTML'))
            self.apartmentSale.setEndDate(endDateElement.get_attribute('innerHTML'))
        except Exception as ex:
            print(ex)

    def excuteCrawl(self):
        self.logger.info(f"Crawling {self.url} ...")

        try:
            self.crawlSale()
            self.crawlApartmentInfo()
            self.crawlApartmentAddress()
            self.crawlApartmentSale()

            return {
                'sale': self.sale.__dict__,
                'apartmentAddress': self.apartmentAddress.__dict__,
                'apartmentInfo': self.apartmentInfo.__dict__,
                'apartmentSale': self.apartmentSale.__dict__,
            }

        except Exception as ex:
            print("Exception: ", ex)

class BatDongSanSearchPageStrategy():
    website: BatDongSanSearchPageWebsite

    def __init__(self, url):
        self.logger = LoggerCustom(BatDongSanStrategy.__name__)
        self.url = url
      
    def changeWebsite(self, url):
        self.website.changeUrl(url)

    def excuteCrawl(self):
        self.logger.info(f"Crawling {self.url} ...")

        self.website = BatDongSanSearchPageWebsiteFactory.create(self.url)

        try:
            elements = self.website.getElementByClass("js__product-link-for-product-id")

            salePostUrls = [element.get_attribute("href") for element in elements]

            return salePostUrls
        except Exception as ex:
            print("Exception: ", ex)
