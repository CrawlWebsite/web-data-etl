from config.envVar import API_HOST, KAFKA_BROKERS
from config.logger import LoggerCustom
from message_queue.index import MessageQueueConsumerImpl
from modules.collector.batdongsan.batdongsanContext import BatDongSanContext
from worker_pool.pool import Pool


def handleCrawlRequest(message):
    context = BatDongSanContext(url='https://batdongsan.com.vn/ban-can-ho-chung-cu-goldsilk-complex')

    context.excuteCrawl()
    

if __name__ == '__main__':
    try:
        logger = LoggerCustom("Main")
        pool = Pool(num_workers=1)

        logger.info("Running")

        queue = MessageQueueConsumerImpl()
        queue.consumerSubcribe('website.crawl', handleCrawlRequest)
    except Exception as ex:
        print(ex)
        logger.error(ex)
        