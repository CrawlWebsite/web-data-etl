from abc import ABC, abstractmethod
from modules.entity.apartment import ApartmentAddress, ApartmentInfo
from modules.entity.apartmentSale import ApartmentSale
from modules.entity.publisher import Publisher

from modules.entity.sale import Sale

class RealEstateData(): 
    sale: Sale
    apartmentAddress: ApartmentAddress
    apartmentInfo: ApartmentInfo
    apartmentSale: ApartmentSale
    publisher: Publisher


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

    @abstractmethod
    def excuteCrawl(self) -> RealEstateData:
        pass
    

    
