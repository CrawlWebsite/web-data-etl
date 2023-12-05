from collector.batdongsan.batdongsanContext import BatDongSanContext
from message_queue.index import MessageQueueImpl
from worker_pool.pool import Pool
from worker_pool.task import Task


def handleCrawlRequest(url):
    print(url)

    context = BatDongSanContext(url='https://batdongsan.com.vn/ban-can-ho-chung-cu-goldsilk-complex')

    context.excuteCrawl()
    

if __name__ == '__main__':
    pool = Pool(num_workers=3)

    queue = MessageQueueImpl()
    queue.consumerSubcribe('website.crawl', handleCrawlRequest)


    # results = pool.get_results()
    # print(results)