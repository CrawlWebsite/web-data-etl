from abc import ABC, abstractmethod

class RealEstateStrategy():
    @abstractmethod
    def changeWebsite(self, url):
        pass

    @abstractmethod
    def crawlSale(self):
        pass

    @abstractmethod
    def crawlApartmentAddress(self):
        pass

    @abstractmethod
    def crawlApartmentInfo(self):
        pass

    @abstractmethod
    def crawlApartmentSale(self):
        pass
    

    
