from urllib.parse import urlparse,urlunparse
from config.logger import LoggerCustom

from modules.collector.batdongsan.batdongsanComposit import BatDongSanComposit
from config import constants

class RealEstateCollector:
    def __init__(self, url, startPage = 1, endPage=30):
        self.logger = LoggerCustom(RealEstateCollector.__name__)

        """
        Extract base url

        Args:
            url (str): The complete URL, e.g., 'https://batdongsan.com/ha-noi'.

        Returns:
            base_url (str): The base URL, e.g., 'https://batdongsan.com'.
        """
        # Parse the URL
        parsed_url = urlparse(url)
        # Get the scheme and netloc
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc
        # Reconstruct the base URL
        self.base_url = urlunparse((scheme, netloc, '', '', '', ''))

        self.url = url
        self.startPage = startPage
        self.endPage = endPage

        # Load search page by base url
        self.loadSearchPage()

    def loadSearchPage(self):
        """
        Create Composite instance by base url
        """

        match self.base_url:
            case constants.BAT_DONG_SAN_HOSTNAME:
                self.realEstateComposit =  BatDongSanComposit(url=self.url)
            case _:
                self.realEstateComposit = None
            
        if self.realEstateComposit is None:
            return
        
        # Add search page from {startPage} to {endPage}
        for page in range(self.startPage, self.endPage + 1):
            self.realEstateComposit.addSearchPage(page)

    def excuteCrawl(self):
        """
        Excute crawl by Real Estate Composit
        """

        if self.realEstateComposit is None:
            self.logger.warn(f"'{self.url}' doesn't match any real state collector")
            return

        self.realEstateComposit.excuteCrawl()