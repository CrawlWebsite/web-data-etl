from config.envVar import API_HOST, KAFKA_BROKERS
from config.logger import LoggerCustom
from message_queue.index import MessageQueueImpl
from modules.collector.batdongsan.batdongsanContext import BatDongSanContext
from worker_pool.pool import Pool


def handleCrawlRequest(message):
    print(message)

    context = BatDongSanContext(url='https://batdongsan.com.vn/ban-can-ho-chung-cu-goldsilk-complex')

    context.excuteCrawl()
    

if __name__ == '__main__':
    print("Running")
    print(KAFKA_BROKERS)
    print(API_HOST)
    logger = LoggerCustom("Main")
    logger.info("Running")
    print("Running")
    pool = Pool(num_workers=3)

    queue = MessageQueueImpl()
    queue.consumerSubcribe('website.crawl', handleCrawlRequest)
