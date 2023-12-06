from collector.batdongsan.batdongsanContext import BatDongSanContext
from config.logger import LoggerCustom


def crawlWebsiteHandler(url, pageStart, pageEnd):
    print(url, pageStart, pageEnd)
    logger = LoggerCustom(BatDongSanContext.__name__)
    logger.info("Crawl")

    context = BatDongSanContext(url=url)
    context.excuteCrawlSalePost(url=url)
    