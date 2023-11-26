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

   
    def crawlName(self):
        name = self.website.crawlName()
        self.sale.setName(name)


    def crawlPhoneNumber(self):
        self.website.crawlPhoneNumber()

    def excuteCrawl(self):
        self.crawlName()
        self.crawlPhoneNumber()