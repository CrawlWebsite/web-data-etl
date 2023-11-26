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
   
    def changeUrl(self, url):
        self.website.changeUrl(url)

    def crawlName(self):
        name = self.website.crawlName()
        self.sale.setName(name)


    def crawlPhoneNumber(self):
        phoneNumber = self.website.crawlPhoneNumber()
        self.sale.setPhoneNumber(phoneNumber)

    def excuteCrawl(self):
        self.crawlName()
        self.crawlPhoneNumber()