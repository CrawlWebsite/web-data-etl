from urllib.parse import urlparse,urlunparse
from config.logger import LoggerCustom

from modules.collector.batdongsan.batdongsanComposit import BatDongSanComposit

class RealEstateCollector:
    def __init__(self, url, startPage = 1, endPage=30):
        self.logger = LoggerCustom(RealEstateCollector.__name__)

        # Parse the URL
        parsed_url = urlparse(url)

        # Get the scheme and netloc
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc

        # Reconstruct the base URL
        self.url = url
        self.base_url = urlunparse((scheme, netloc, '', '', '', ''))

        self.startPage = startPage
        self.endPage = endPage

        self.loadSearchPage()

    def loadSearchPage(self):
        match self.base_url:
            case 'https://batdongsan.com.vn':
                self.realEstateCollector =  BatDongSanComposit(url=self.url)
            case _:
                self.realEstateCollector = None
            
        if self.realEstateCollector is None:
            return
        
        for page in range(self.startPage, self.endPage + 1):
            self.realEstateCollector.addSearchPage(page)

    def excuteCrawl(self):
        if self.realEstateCollector is None:
            self.logger.warn(f"'{self.url}' doesn't match any real state collector")
            return

        self.realEstateCollector.excuteCrawl()