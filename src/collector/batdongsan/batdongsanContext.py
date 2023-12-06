from collector.batdongsan.batdongsanStrategy import BatDongSanStrategy
from selenium.webdriver.common.by import By
from worker_pool.pool import Pool

from worker_pool.task import Task


class BatDongSanContext:
    mainStrategy: BatDongSanStrategy

    salePostStrategy: BatDongSanStrategy
    salePostUrls: list

    def __init__(self, url):
        self.pool = Pool()
        self.mainStrategy = BatDongSanStrategy(url=url)
        self.salePostStrategy = None


    def setSalePostStrategy(self, strategy):
        self.salePostStrategy = strategy

    def crawlSalePostUrls(self):
        elements = self.mainStrategy.website.getElementByClass("js__product-link-for-product-id")
        self.salePostUrls = [element.get_attribute("href") for element in elements]
        print(self.salePostUrls)

    def excuteCrawl(self):
        self.crawlSalePostUrls()

        for salePostUrl in self.salePostUrls:
            url_new = salePostUrl.replace('http://localhost:3000','https://batdongsan.com.vn')

           
            self.pool.add_task(Task(url_new, self.excuteCrawlSalePost, args=(url_new,)))

    def excuteCrawlSalePost(self, url):
        salePostStrategy = BatDongSanStrategy(url=url)
        
        salePostStrategy.excuteCrawl()
