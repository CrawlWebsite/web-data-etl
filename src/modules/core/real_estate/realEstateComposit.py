from abc import ABC, abstractmethod

class RealEstateComposit():
    @abstractmethod
    def extractSearchPageUrl(self, url):
        pass

    @abstractmethod
    def addSearchPage(self, page):
        pass

    @abstractmethod
    def excuteCrawl(self):
        pass
    
    @abstractmethod
    def excuteCrawlSalePost(self, salePostUrl):
        pass
    
    
