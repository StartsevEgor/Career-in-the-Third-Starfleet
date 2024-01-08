from additional_functions import *

files = {
    "map": "data/map.txt",
    "Civilian ship": "data/Objects/Ships/Civilian ship/civilian ship.txt"
}


class Object:
    def __init__(self, class_):
        self.class_ = class_
        self.data = unpacking_txt(files[class_])
        self.width = self.data["Width"]
        self.height = self.data["Height"]
        self.mass = self.data["Mass"]
        self.buy_price = self.data["Buy price"]
        self.sell_price = self.data["Sell price"]
        self.file_with_image = files[self.class_]


class Ship(Object):
    def __init__(self, class_):
        super().__init__(class_)
        self.level = self.data["Level"]
        self.energy = self.data["Energy"]
        self.energy_recovery_rate = self.data["Energy recovery rate"]
        self.shield = self.data["Shield"]
        self.armor = self.data["Armor"]
        self.standard_speed = self.data["Standard speed"]
        self.acceleration_time = self.data["Acceleration_time"]


class Module(Object):
    def __init__(self, class_):
        super().__init__(class_)
        self.level = self.data["Level"]
        self.type = self.data["Type"]

class System:
    def __init__(self, name, data):

class Map:
    def __init__(self):
        self.data = unpacking_txt_to_map(files["map"])
        for system in self.data.keys():



civilian_ship = Ship("Civilian ship")
map = unpacking_txt_to_map("data/map.txt")
print(map)
main_character = unpacking_txt("data/Objects/Characters/main_character/main_character.txt")
