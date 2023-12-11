import json
import re

import attr
from config.envVar import API_HOST
from config.logger import LoggerCustom
from message_queue.index import MessageQueueProducerImpl
from modules.collector.batdongsan.batdongsanStrategy import BatDongSanSearchPageStrategy, BatDongSanStrategy
from modules.core.real_estate.realEstateComposit import RealEstateComposit
from worker_pool.pool import Pool

from worker_pool.task import Task


class BatDongSanComposit(RealEstateComposit):
    hostname = "https://batdongsan.com.vn"
    urlPattern = re.compile(r"https://batdongsan\.com\.vn/[^/]+")
    paginationPattern = "/p{}"

    def __init__(self, url):
        self.logger = LoggerCustom(BatDongSanComposit.__name__)
        
        self.pool = Pool()
        self.message_queue = MessageQueueProducerImpl()

        self.searchPageUrl = self.extractSearchPageUrl(url)

        self.searchPagesStrategy: list[BatDongSanSearchPageStrategy] = []

    def extractSearchPageUrl(self, url):
        extractUrl = re.search(self.urlPattern, url)

        if extractUrl:
            return extractUrl.group(0)
        else:
            return

    def addSearchPage(self, page):
        if self.searchPageUrl is None:
            self.logger.warn("No search page")
            return
        
        self.logger.info(f"Add search page {self.searchPageUrl} - {page} ...")

        url = self.searchPageUrl + self.paginationPattern.format(page)
        self.searchPagesStrategy.append(BatDongSanSearchPageStrategy(url=url))

    def excuteCrawl(self):
        for searchPageStrategy in self.searchPagesStrategy:
            # Get all sale post urls in search page
            salePostUrls = searchPageStrategy.excuteCrawl()

            for salePostUrl in salePostUrls:
                salePostUrl = salePostUrl.replace(API_HOST, self.hostname)


                self.pool.add_task(Task(salePostUrl, self.excuteCrawlSalePost, args=(salePostUrl,)))

    def excuteCrawlSalePost(self, salePostUrl):
        salePostStrategy = BatDongSanStrategy(url=salePostUrl)
        
        data = salePostStrategy.excuteCrawl()
        print(data)
        self.message_queue.sendMessage('website.crawl.data', data)
