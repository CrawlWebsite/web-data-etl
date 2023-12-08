from config.envVar import API_HOST
from message_queue.index import MessageQueueProducerImpl
from modules.collector.batdongsan.batdongsanStrategy import BatDongSanStrategy
from worker_pool.pool import Pool

from worker_pool.task import Task


class BatDongSanContext:
    mainStrategy: BatDongSanStrategy

    salePostStrategy: BatDongSanStrategy
    salePostUrls: list

    def __init__(self, url):
        self.pool = Pool()
        self.message_queue = MessageQueueProducerImpl()
        self.mainStrategy = BatDongSanStrategy(url=url)
        self.salePostStrategy = None


    def setSalePostStrategy(self, strategy):
        self.salePostStrategy = strategy

    def crawlSalePostUrls(self):
        elements = self.mainStrategy.website.getElementByClass("js__product-link-for-product-id")

        self.salePostUrls = [element.get_attribute("href") for element in elements]

    def excuteCrawl(self):
        self.crawlSalePostUrls()
        print(self.salePostUrls)
        for salePostUrl in self.salePostUrls:
            url_new = salePostUrl.replace(API_HOST,'https://batdongsan.com.vn')

           
            self.pool.add_task(Task(url_new, self.excuteCrawlSalePost, args=(url_new,)))

    def excuteCrawlSalePost(self, url):
        salePostStrategy = BatDongSanStrategy(url=url)
        
        data = salePostStrategy.excuteCrawl()

        print(data)
        self.message_queue.sendMessage('website.crawl.data', data)
