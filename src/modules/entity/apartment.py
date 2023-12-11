from enum import Enum

class LegalStatus(Enum):
    LAND_TITLE_DEED = 'land_title_deed'
    SALE_AGREEMENT = 'sale_agreement'
    OTHER = 'other'

class ApartmentAddress:
    city: str
    district: str
    address: str
    project: str

    def setCity(self, city):
        self.city = city

    def getCity(self):
        return self.city

    def setDistrict(self, district):
        self.district = district

    def getDistrict(self):
        return self.district

    def setAddress(self, address):
        self.address = address
    
    def getAddress(self):
        return self.address
    
    def setProject(self, project):
        self.project = project

    def getProject(self):
        return self.project

class ApartmentInfo:
    acreage: str
    acreageUnit: str
    type: str
    legal: str
    legalStatus: str
    apartmentFloor: int
    numberOfBedRoom: int
    numberOfToilet: int
    numberOfFloor: int
    pricePerSquareMeter: str
    pricePerSquareMeterUnit: str
    price: str
    priceUnit: str
    balconyDirection: str
    apartmentDirection: str
    interior: str

    def setAcreage(self, acreageText):
        if acreageText is not None:
            self.acreage, self.acreageUnit = acreageText.split(" ")

    def getAcreage(self):
        return self.acreage
    
    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setLegal(self, legal):
        self.legal = legal
        match legal:
            case 'Sổ đỏ/ Sổ hồng':
                self.legalStatus = LegalStatus.LAND_TITLE_DEED.value
            case 'Hợp đồng mua bán':
                self.legalStatus = LegalStatus.SALE_AGREEMENT.value
            case _:
                self.legalStatus = LegalStatus.OTHER.value

    def setApartmentFloor(self, apartmentFloor):
        self.apartmentFloor = apartmentFloor

    def getApartmentFloor(self):
        return self.apartmentFloor

    def setNumberOfBedRoom(self, numberOfBedRoom):
        if numberOfBedRoom is not None:
            self.numberOfBedRoom = numberOfBedRoom.split(' ')[0]

    def getNumberOfBedRoom(self):
        return self.numberOfBedRoom

    def setNumberOfToilet(self, numberOfToilet):
        if numberOfToilet is not None:
            self.numberOfToilet = numberOfToilet.split(' ')[0]

    def getNumberOfToilet(self):
        return self.numberOfToilet

    def setPricePerSquareMeter(self, pricePerSquareMeter):
        if pricePerSquareMeter is not None:
            self.pricePerSquareMeter, self.pricePerSquareMeterUnit = pricePerSquareMeter.split(' ')

    def getPricePerSquareMeter(self):
        return self.pricePerSquareMeter

    def setNumberOfFloor(self, numberOfFloor):
        self.numberOfFloor = numberOfFloor

    def getNumberOfFloor(self):
        return self.numberOfFloor
    
    def setPrice(self, price):
        if price is not None:
            print(price)
            self.price, self.priceUnit = price.split(' ')

    def getPrice(self):
        return self.price
    
    def setBalconyDirection(self, balconyDirection):
        self.balconyDirection = balconyDirection

    def getBalconyDirection(self):
        return self.balconyDirection
    
    def setApartmentDirection(self, apartmentDirection):
        self.apartmentDirection = apartmentDirection

    def getApartmentDirection(self):
        return self.apartmentDirection
    
    def setInterior(self, interior):
        self.interior = interior

    def getInterior(self):
        return self.interior