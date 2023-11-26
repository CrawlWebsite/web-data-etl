from core.website.website import Website
from entity.sale import Sale


class BatDongSanWebsite(Website):
    def __init__(self, url):
        super().__init__(url)

    def crawlName(self):
        nameElement = self.getElementByCssSelector("div.re__contact-name.js_contact-name")
        name = nameElement[0].get_attribute('title')

        return name

    def crawlPhoneNumber(self):
        # element = super().getElementByClass()
        pass

    def excuteCrawl(self):
        self.crawlName()
        # self.crawlPhoneNumber()


class BatDongSanWebsiteFactory(Website):
    def create(url):
        return BatDongSanWebsite(url)
   