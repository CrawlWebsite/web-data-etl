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
    type: str
    juridical: str
    apartmentFloor: int
    numberOfBedRoom: int
    numberOfToilet: int
    numberOfFloor: int
    pricePerSquareMeter: str
    price: str
    balconyDirection: str
    apartmentDirection: str
    interior: str

    def setAcreage(self, acreage):
        self.acreage = acreage

    def getAcreage(self):
        return self.acreage
    
    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setJuridical(self, juridicalType):
        self.juridicalType = juridicalType

    def getJuridical(self):
        return self.juridicalType

    def setApartmentFloor(self, apartmentFloor):
        self.apartmentFloor = apartmentFloor

    def getApartmentFloor(self):
        return self.apartmentFloor

    def setNumberOfBedRoom(self, numberOfBedRoom):
        self.numberOfBedRoom = numberOfBedRoom

    def getNumberOfBedRoom(self):
        return self.numberOfBedRoom

    def setNumberOfToilet(self, numberOfToilet):
        self.numberOfToilet = numberOfToilet

    def getNumberOfToilet(self):
        return self.numberOfToilet

    def setPricePerSquareMeter(self, pricePerSquareMeter):
        self.pricePerSquareMeter = pricePerSquareMeter

    def getPricePerSquareMeter(self):
        return self.pricePerSquareMeter

    def setNumberOfFloor(self, numberOfFloor):
        self.numberOfFloor = numberOfFloor

    def getNumberOfFloor(self):
        return self.numberOfFloor
    
    def setPrice(self, price):
        self.price = price

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