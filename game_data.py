from additional_functions import *

files = {
    "map": "data/map.txt",
    "Civilian ship": "data/Objects/Ships/Civilian ship/civilian ship.txt",
    "Civilian ship Image": "data/Objects/Ships/Civilian ship/civilian ship.png"
}
all_sprites = pygame.sprite.Group()

class Object(Standart_Sprite):
    def __init__(self, class_, coordinates):
        self.x, self.y = coordinates
        self.class_ = class_
        self.data = unpacking_txt(files[class_])
        self.type_ = self.data["Type"]
        self.width = float(self.data["Width"])
        self.height = float(self.data["Height"])
        self.mass = float(self.data["Mass"])
        self.buy_price = self.data["Buy price"]
        self.sell_price = self.data["Sell price"]
        self.file_with_image = files[self.class_ + " Image"]
        super().__init__(self.width, self.height, self.x, self.y, all_sprites)
    # def update(self, new_width=None, new_height=None, new_x=None, new_y=None, new_approximation_factor=None):
    #     super().update(new_width, new_height, new_x, new_y, new_approximation_factor)
    #     self.width = new_width if new_width else self.width
    #     self.height = new_height if new_height else self.height
    #     self.x = new_x if new_x else self.x
    #     self.y = new_y if new_y else self.y
    #     self.image = pygame.transform.scale(self.image, (self.width, self.height))
    #     self.rect = self.image.get_rect()
    #     self.rect.x = self.x
    #     self.rect.y = self.y



    def __str__(self):
        return self.class_


class Ship(Object):
    def __init__(self, class_, coordinates):
        super().__init__(class_, coordinates)
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


class Star:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates

    def __str__(self):
        return self.name


class Planet:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates

    def __str__(self):
        return self.name


class Character:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.file_name = f"data/Objects/Characters/{self.name}/{self.name}.txt"
        self.data = unpacking_txt(self.file_name)
        self.name = self.data["Name"]
        self.hp = self.data["HP"]
        self.level = self.data["Level"]
        self.items = self.data["Items"]
        self.main_ship = Ship(self.data["Main ship"], self.coordinates)
        self.data["Ships"].remove(self.data["Main ship"])
        # self.ships = list(map(lambda ship: Ship(ship), self.data["Ships"]))
        # self.ships.append(self.main_ship)
        print(self.main_ship)

    def __str__(self):
        return self.name


class System:
    def __init__(self, name, objects):
        self.name = name
        self.stars = []
        self.planets = []
        self.characters = []
        for object in objects.keys():
            type_, name = object.split()[0], " ".join(object.split()[1:])
            if type_ == "Star":
                self.stars.append(Star(name, objects[object]))
            elif type_ == "Planet":
                self.planets.append(Planet(name, objects[object]))
            elif type_ == "Character":
                self.characters.append(Character(name, objects[object]))

    def search(self, request, type_=None, accurate_search=False):
        result = {"Star": [], "Planet": [], "Character": []}
        if type_ == "star" or type_ is None:
            for star in self.stars:
                if request in str(star):
                    if accurate_search:
                        return star
                    result["Star"].append(star)
        if type_ == "planet" or type_ is None:
            for planet in self.planets:
                if request in str(planet):
                    if accurate_search:
                        return planet
                    result["Planet"].append(planet)
        if type_ == "character" or type_ is None:
            for character in self.characters:
                if request in str(character):
                    if accurate_search:
                        return character
                    result["Character"].append(character)
        return result


class Map:
    def __init__(self):
        self.data_in_dictionary = unpacking_txt_to_map(files["map"])
        self.data = []
        for system in self.data_in_dictionary.keys():
            self.data.append(System(system, self.data_in_dictionary[system]))

    def search(self, request, type_=None, accurate_search=False):
        result = {}
        for system in self.data:
            system_result = system.search(request, type_, accurate_search)
            result[str(system)] = system_result
            if accurate_search:
                return system_result
        return result


map_in_dictionary = unpacking_txt_to_map(files["map"])
map_ = Map()
