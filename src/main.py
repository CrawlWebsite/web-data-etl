from collector.batdongsan.batdongsanContext import BatDongSanContext
from message_queue.index import MessageQueueImpl
from worker_pool.pool import Pool
from worker_pool.task import Task


def handleCrawlRequest(url):
    print(url)
    # context = BatDongSanContext(url='https://batdongsan.com.vn/ban-can-ho-chung-cu-goldsilk-complex')

    pool = Pool()
    tasks = [Task(square, (i,)) for i in range(1)]
    for task in tasks:
        pool.submit(task)

    # context.excuteCrawl()
    
def square(x):
    return x ** 2

if __name__ == '__main__':
    pool = Pool(num_workers=4)
    pool.start()

    queue = MessageQueueImpl()
    queue.consumerSubcribe('website.crawl', handleCrawlRequest)

    pool.join()

    results = pool.get_results()
    print(results)