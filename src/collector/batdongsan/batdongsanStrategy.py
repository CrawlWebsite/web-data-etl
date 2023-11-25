from core.real_estate.realEstateStrategy import RealEstateStrategy
from src.collector.batdongsan.batdongsanWebsite import BatDongSanWebsite, BatDongSanWebsiteFactory


class BatDongSanStrategy(RealEstateStrategy):
    website: BatDongSanWebsite

    def __init__(self, url):
        self.website = BatDongSanWebsiteFactory.create(url)
   
    def getPageContent():
        super().getPageContent()

    def crawlName():
        super().crawlName()

    def crawlPhoneNumber():
        super().crawlPhoneNumber()