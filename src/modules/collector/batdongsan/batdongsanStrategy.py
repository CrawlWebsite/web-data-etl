import re
from config.logger import LoggerCustom
from selenium.webdriver.common.by import By 

from modules.core.web_driver.webDriver import WebDriver
from modules.core.real_estate.realEstateStrategy import RealEstateData, RealEstateStrategy

from modules.entity.apartment import ApartmentAddress, ApartmentInfo
from modules.entity.apartmentSale import ApartmentSale
from modules.entity.sale import Sale

from modules.collector.batdongsan.batdongsanWebsite import BatDongSanSearchPageWebsite, BatDongSanSearchPageWebsiteFactory, BatDongSanWebsite, BatDongSanWebsiteFactory
from utils.numberFormat import stringToNumber
from config import constants


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
        """
        Change website url and get new page content

        Args:
            url (str): url to change
        """
        self.website.changeUrl(url)

    def crawlSale(self):
        """
        Crawl sale data in sale post
        """

        try:
            self.logger.info("Crawling sale ...")

            # Crawl name
            self.crawlName()

            # Crawl phone number
            self.crawlPhoneNumber()

            self.logger.info(f"Crawling sale successfully: {self.sale.__dict__}")
        except Exception as ex:
            print(ex)

    def crawlApartmentAddress(self):
        """
        Crawl apartment address in sale post
        """

        try:
            self.logger.info("Crawling apartment address ...")

            """
            Crawl city, district
            Get address elements
            HTML e.g.: 
                <div class="js__breadcrumb">
                    <a level="1"></a>
                    <a level="1"></a>
                </div>
            """
            addressElements = self.website.getElementByCssSelector(css_selector='div.js__breadcrumb a')
            """
            Crawl data by level of each element
            """
            for addressElement in addressElements:
                level = addressElement.get_attribute('level')
                value = addressElement.get_attribute('innerHTML')

                # Update apartment address by level of each element
                self.updateApartmentAddressByLevel(level, value)
        
            """
            Crawl project
            Get project element
            HTML e.g.: 
                <div class="re__project-title"></div>
            """
            projectElement = self.website.getElementByCssSelector(css_selector='div.re__project-title')
            if len(projectElement) > 0:

                # Get project via innerHTML of element
                project = projectElement[0].get_attribute('innerHTML')
                # Update project
                self.apartmentAddress.setProject(project)

            """
            Crawl address
            Get address element
            HTML e.g.: 
                <span class="js__pr-address"></span>
            """
            addressElement = self.website.getElementByCssSelector(css_selector='span.js__pr-address')
            if len(addressElement) > 0:
                # Get address via innerHTML of element
                address = addressElement[0].get_attribute('innerHTML')
                # Update address
                self.apartmentAddress.setAddress(address)

            self.logger.info(f"Crawling apartment address successfully: {self.apartmentAddress.__dict__}")
        except Exception as ex:
            print(ex)

    def crawlApartmentInfo(self):
        """
        Crawl apartment information in sale post
        """

        try:
            self.logger.info("Crawling apartment information ...")

            """
            Get information element: acreage, direction, ...
            HTML e.g.:
                <div class="re__pr-specs-content-item">
                    <span>
                        <i class="info"></i>
                    </span>
                    <span class="re__pr-specs-content-item-value">Info</span>
                </div>
            """
            infoElements = self.website.getElementByCssSelector(css_selector='div.re__pr-specs-content-item')
            
            for infoElement in infoElements:
                # Get icon element
                iconElement = infoElement.find_elements(By.CSS_SELECTOR, 'span i')
                # Get icon class
                if len(iconElement) > 0:
                    iconClass = iconElement[0].get_attribute('class')
                else:
                    iconClass = ''

                # Get value element
                valueElement = infoElement.find_elements(By.CSS_SELECTOR, 'span.re__pr-specs-content-item-value')
                # Get value via innerHTML of element
                if len(valueElement) > 0:
                    value = valueElement[0].get_attribute('innerHTML')
                else: 
                    value = None

                # Update apartment infomation by icon class
                self.updateApartmentInfoByIconClass(iconClass, value)

            """
            Get information element: price
            HTML e.g.:
                <div class="re__pr-short-info-item js__pr-short-info-item">
                    <span class="value"></span>
                    <span class="ext"></span>
                    <span></span>
                </div>
            """
            # Get price wrap element
            priceWrapElement = self.website.getElementByCssSelector(css_selector='div.re__pr-short-info-item.js__pr-short-info-item')
            # Get list of span element in first wrap element
            if len(priceWrapElement) > 0:
                priceValueElements = priceWrapElement[0].find_elements(By.CSS_SELECTOR, 'span')
            else:
                priceValueElements = None

            # If there are 3 span elements in wrap element, it is price information
            if len(priceValueElements) == 3:
                for priceValueElement in priceValueElements:
                    # Element with class "value" is price information
                    if priceValueElement.get_attribute('class') == 'value':
                        value = priceValueElement.get_attribute("innerHTML")
                        # String value includes price and priceUnit. E.g. "2 ty"
                        price, priceUnit = value.split(' ')

                        self.apartmentInfo.setPrice(stringToNumber(price))
                        self.apartmentInfo.setPriceUnit(priceUnit)

                    # Element with class "ext" is pricePerSquareMeter information
                    if priceValueElement.get_attribute('class') == 'ext':
                        value = priceValueElement.get_attribute("innerHTML")
                        # String value includes price and priceUnit. E.g. "~20 tr/m2"
                        pricePerSquareMeter, pricePerSquareMeterUnit = value.split(' ')
                       
                        # Remove "~" at the beginning of pricePerSquareMeter
                        self.apartmentInfo.setPricePerSquareMeter(stringToNumber(pricePerSquareMeter[1:]))
                        self.apartmentInfo.setPricePerSquareMeterUnit(pricePerSquareMeterUnit)

            
            self.logger.info(f"Crawling apartment information successfully: {self.apartmentInfo.__dict__}")
        except Exception as ex:
            print(ex)

    def crawlName(self):
        """
        Crawl sale name
        HTML e.g.
            <div class="re__contact-name js_contact-name" title="name"></div>
        """

        # Get name element
        nameElement = self.website.getElementByCssSelector("div.re__contact-name.js_contact-name")

        if len(nameElement) > 0:
            # Get name via title of element
            name = nameElement[0].get_attribute('title')

            # Update name
            self.sale.setName(name)


    def crawlPhoneNumber(self):
        """
        Crawl sale phone number
        HTML e.g.
            <div class="phone js__phone" raw="phoneNumberRaw"></div>

        Specifically, we only get the phone number raw in sale post, so we need to call API to decrypt the phone number raw
        To decrypt, we create new page with decrypte url and crawl from it
        """
        
        # Get phone raw element
        phoneElement = self.website.getElementByCssSelector("div.phone.js__phone")

        if len(phoneElement) == 0:
            return ''
        
        # Get phone number raw
        phoneRaw = phoneElement[0].get_attribute('raw')

        # Create new page with decrypt url
        self.phoneDecryptDriver.getPageContent(cmd='post', url_crawl=self.phoneDecryptUrl, postData=f'PhoneNumber={phoneRaw}')

        # Get phone number element
        phoneNumberElement = self.phoneDecryptDriver.getElementByCssSelector(css_selector='pre')

        # Get phone number via innerHTML of element
        if len(phoneNumberElement) > 0:
            phoneNumber = re.sub(r'\s', '', phoneNumberElement[0].get_attribute('innerHTML'))
        else:
            phoneNumber = None

        # Update phone number
        self.sale.setPhoneNumber(phoneNumber)

    def updateApartmentAddressByLevel(self, level, value):
        """
        Update the apartment address by level of element
        Element level: 
            2: city
            3: district

        Args:
            level (str): the level of element
            value (str): innerHTML of element
        """

        match level:
            case "2":
                self.apartmentAddress.setCity(value)
            case "3":
                self.apartmentAddress.setDistrict(value)

    def updateApartmentInfoByIconClass(self, iconClass, value):
        """
        Update apartment information by icon class
        
        Args:
            iconClass (str): the icon class
            value (str): innerHTML of element
        """

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
        """
        Crawl apartment sale information
        """

        try:
            self.logger.info("Crawling apartment sale ...")

            # Update sale post url
            self.apartmentSale.setUrl(self.url)

            """
            Crawl sale post date
            HTML e.g.:
                <div class="re__pr-short-info-item js__pr-config-item">
                    <span class="value"></span>
                </div>
                <div class="re__pr-short-info-item js__pr-config-item">
                    <span class="value"></span>
                </div>
                ...

            The first 2 elements will be startDate and endDate
            """
            startDateElement, endDateElement = self.website.getElementByCssSelector("div.re__pr-short-info-item.js__pr-config-item span.value")[:2]

            self.apartmentSale.setStartDate(startDateElement.get_attribute('innerHTML'))
            self.apartmentSale.setEndDate(endDateElement.get_attribute('innerHTML'))
        except Exception as ex:
            print(ex)

    def excuteCrawl(self) -> RealEstateData:
        """
        Excute crawl apartment information
        """

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
                'publisher': {
                    'hostname': constants.BAT_DONG_SAN_HOSTNAME
                }
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
        """
        Excute crawl search page information
        """

        self.logger.info(f"Crawling {self.url} ...")

        self.website = BatDongSanSearchPageWebsiteFactory.create(self.url)

        try:
            """
            Get search page information
            HTML e.g.:
                <a class="js__product-link-for-product-id" href="http://batdongsan"></a>
                <a class="js__product-link-for-product-id" href="http://batdongsan"></a>
                ...
            """
            elements = self.website.getElementByClass("js__product-link-for-product-id")

            # Get sale post url via href of element
            salePostUrls = [element.get_attribute("href") for element in elements]

            return salePostUrls
        except Exception as ex:
            print("Exception: ", ex)
