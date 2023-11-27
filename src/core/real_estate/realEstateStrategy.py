from abc import ABC, abstractmethod
class RealEstateStrategy(ABC):
    @abstractmethod
    def changeWebsite(self, url):
        pass

    @abstractmethod
    def crawlName(self):
        pass

    @abstractmethod
    def crawlPhoneNumber(self):
        pass
