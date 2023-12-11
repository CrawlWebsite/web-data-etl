from config.envVar import API_HOST, KAFKA_BROKERS
from config.logger import LoggerCustom
from message_queue.index import MessageQueueConsumerImpl
from modules.collector.realEstateCollector import RealEstateCollector
from worker_pool.pool import Pool


def handleCrawlRequest(message):
    print(message)
    url = message.value.get('url')
    startPage = message.value.get('startPage') or 1
    endPage = message.value.get('endPage') or 30

    if url is None:
        return

    collector = RealEstateCollector(url=url, startPage=startPage, endPage=endPage)
    collector.excuteCrawl()
    
    return
    

if __name__ == '__main__':
    try:
        logger = LoggerCustom("Main")
        pool = Pool(num_workers=3)

        logger.info("Running")

        queue = MessageQueueConsumerImpl()
        queue.consumerSubcribe('website.crawl.register', handleCrawlRequest)

    except Exception as ex:
        print(ex)
        logger.error(ex)
        