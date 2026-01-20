class ElectricVehicle:
    def __init__(self, regnum, make, model, color):
        self.color = color
        self.regnum = regnum
        self.make = make
        self.model = model
        self.charge = 0

    def getMake(self):
        return self.make

    def getModel(self):
        return self.model

    def getColor(self):
        return self.color

    def getRegNum(self):
        return self.regnum

    def setCharge(self, charge):
        self.charge = charge

    def getCharge(self):
        return self.charge


# ✅ NOW they are real subclasses
class ElectricCar(ElectricVehicle):
    def __init__(self, regnum, make, model, color):
        super().__init__(regnum, make, model, color)

    def getType(self):
        return "Car"


class ElectricBike(ElectricVehicle):
    def __init__(self, regnum, make, model, color):
        super().__init__(regnum, make, model, color)

    def getType(self):
        return "Motorcycle"
