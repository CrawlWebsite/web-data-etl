from collector.batdongsan.batdongsanContext import BatDongSanContext
from message_queue.index import MessageQueueImpl



def handleCrawlRequest(url):
    print(url)
    context = BatDongSanContext(url='https://batdongsan.com.vn/ban-can-ho-chung-cu-goldsilk-complex')

    context.excuteCrawl()

queue = MessageQueueImpl()
queue.consumerSubcribe('website.crawl', handleCrawlRequest)