from math import *
from additional_functions import *
from random import randint


class Ship:
    def __init__(self):
        self.angle_of_rotation = 0
        self.speed = 0
        self.x_speed = 0
        self.y_speed = 0


class Civilian_ship(Ship):
    def __init__(self, name, x, y, sprite_group):
        super().__init__()
        self.id = randint(1, 1000000)
        self.name = name
        self.x, self.y = x, y
        self.type_ = "Истребитель"
        self.width = 55
        self.height = 50
        self.mass = 79000000
        self.buy_price = 0
        self.sell_price = 0
        self.file_with_image = "data/Objects/Ships/Civilian ship/civilian ship.png"
        self.level = 1
        self.energy = 2000000000
        self.energy_recovery_rate = 8777777
        self.shield = 1000000000
        self.armor = 1000000000
        self.max_speed = 400
        self.acceleration_time = 6.5
        self.boost = self.max_speed / self.acceleration_time
        self.image = load_image(self.file_with_image, colorkey=-1)

    def move(self, time, type_="Boost"):
        self.speed = self.speed + self.boost * time if 0 <= self.speed + self.boost * time <= 400 else (
            0 if self.speed + self.boost * time < 0 else 400)
        self.x_speed = self.speed * sin(radians(self.angle_of_rotation))
        self.y_speed = self.speed * cos(radians(self.angle_of_rotation))
        self.x += self.x_speed + time
        self.y += self.y_speed + time

    def __str__(self):
        return self.name


class Module:
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
