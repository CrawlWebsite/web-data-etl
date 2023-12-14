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
from config import constants


class BatDongSanComposit(RealEstateComposit):
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
        """
        Add SearchPageStrategy instance to list

        Args:
            page (int): page number
        """
        
        if self.searchPageUrl is None:
            self.logger.warn("No search page")
            return
        
        self.logger.info(f"Add search page {self.searchPageUrl} - {page} ...")

        url = self.searchPageUrl + self.paginationPattern.format(page)
        self.searchPagesStrategy.append(BatDongSanSearchPageStrategy(url=url))

    def excuteCrawl(self):
        """
        Excute crawl
        """

        """
        Loop search pages and add excute crawl task of each page to thread pool
        """
        for searchPageStrategy in self.searchPagesStrategy:
            # Get all sale post urls in search page
            salePostUrls = searchPageStrategy.excuteCrawl()

            """
            When crawl sale post urls,
                we get hostname of each sale post url is the hostname of backend service
            So we need to replace to the hostname of real estate website
            """
            for salePostUrl in salePostUrls:
                salePostUrl = salePostUrl.replace(API_HOST, constants.BAT_DONG_SAN_HOSTNAME)

                # Add excute crawl task to thread pool
                self.pool.add_task(Task(salePostUrl, self.excuteCrawlSalePost, args=(salePostUrl,)))

    def excuteCrawlSalePost(self, salePostUrl):
        """
        Crawl sale post url

        Args:
            salePostUrl (str): url of sale post

        Returns:
            Send crawl data to kafka topic
        """

        salePostStrategy = BatDongSanStrategy(url=salePostUrl)
        
        data = salePostStrategy.excuteCrawl()

        self.logger.info(f'Crawl succeeded {data}')
        self.message_queue.sendMessage('website.crawl.data', data)
