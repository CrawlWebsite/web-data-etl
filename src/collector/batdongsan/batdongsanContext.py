from collector.batdongsan.batdongsanStrategy import BatDongSanStrategy
from selenium.webdriver.common.by import By 
from core.real_estate.realEstateStrategy import RealEstateStrategy
from collector.batdongsan.batdongsanWebsite import BatDongSanWebsite, BatDongSanWebsiteFactory


class BatDongSanContext:
    mainStrategy: BatDongSanStrategy

    salePostStrategy: BatDongSanStrategy
    salePostUrls: list

    def __init__(self, url):
        self.mainStrategy = BatDongSanStrategy(url=url)

    def setSalePostStrategy(self, strategy):
        self.salePostStrategy = strategy

    def crawlSalePostUrls(self):
        elements = self.mainStrategy.website.getElementByClass("js__product-link-for-product-id")
        self.salePostUrls = [element.get_attribute("href") for element in elements]
        print(self.salePostUrls)

    def excuteCrawl(self):
        for salePostUrl in self.salePostUrls:
            url_new = salePostUrl.replace('http://localhost:3000','https://batdongsan.com.vn')

            print(url_new)
            strategy = BatDongSanStrategy(url=url_new)
            self.setSalePostStrategy(strategy=strategy)
            self.salePostStrategy.excuteCrawl()
            print(self.salePostStrategy.sale)
