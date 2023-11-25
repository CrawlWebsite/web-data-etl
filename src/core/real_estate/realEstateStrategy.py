from core.real_estate.realEstateWebsite import RealEstateWebsite
from src.core.website.website import Website

class RealEstateStrategy:
    website: RealEstateWebsite

    def __init__(self):
        super().__init__()

    def crawlName(self):
        self.website.crawlName()

    def crawlPhoneNumber(self):
        self.website.crawlPhoneNumber()

    def getPageContent(self):
        self.website.getPageContent()