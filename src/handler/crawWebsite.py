from collector.batdongsan.batdongsanContext import BatDongSanContext


def crawlWebsiteHandler(url, pageStart, pageEnd):
    print(url, pageStart, pageEnd)
    context = BatDongSanContext(url=url)
    context.excuteCrawlSalePost(url=url)
    