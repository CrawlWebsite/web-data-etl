from src.core.website.website import Website


class IRealEstateStrategy:
    def crawlName():
        pass
    def crawlPhoneNumber():
        pass

class RealEstateStrategy(IRealEstateStrategy):
    def __init__(self):
        super().__init__()
        self.website = Website()

    def crawlName():
        self.website.crawlName()

    def crawlPhoneNumber():
        pass