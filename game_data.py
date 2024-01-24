from math import *
from additional_functions import *
from random import randint

ships_settings = {
    "Civilian ship": {"type": "Истребитель", "type_image": "", "width": 50, "height": 55, "mass": 79000000,
                      "buy_price": 0,
                      "sell_price": 0, "file_with_image": "data/Objects/Ships/Civilian ship/civilian ship.png",
                      "file_with_icon_image":
                          "C:/Users/start/PycharmProjects/pythonProject1/data/Objects/Mini images/ship.png",
                      "level": 1, "energy": 2000000000, "energy_recovery_rate": 8777777, "shield": 1000000000,
                      "armor": 1000000000, "max_speed": 400, "acceleration_time": 1.5, "braking_time": 1,
                      "max_rotate_speed": 120, "acceleration_rotate_time": 0.5}
}


class Ship:
    def __init__(self, name, x, y, settings):
        super().__init__()
        self.name = name
        self.x, self.y = x, y
        self.angle_of_rotation = 0
        self.rotate_speed = 0
        self.speed = 0
        self.x_speed = 0
        self.y_speed = 0
        self.type_ = settings["type"]
        self.width = settings["width"]
        self.height = settings["height"]
        self.mass = settings["mass"]
        self.buy_price = settings["buy_price"]
        self.sell_price = settings["sell_price"]
        self.file_with_image = settings["file_with_image"]
        self.file_with_icon_image = settings["file_with_icon_image"]
        self.level = settings["level"]
        self.energy = settings["energy"]
        self.energy_recovery_rate = settings["energy_recovery_rate"]
        self.gamage_energy = 0
        self.shield = settings["shield"]
        self.armor = settings["armor"]
        self.max_speed = settings["max_speed"]
        self.acceleration_time = settings["acceleration_time"]
        self.braking_time = settings["braking_time"]
        self.max_rotate_speed = settings["max_rotate_speed"]
        self.acceleration_rotate_time = settings["acceleration_rotate_time"]
        self.rotate_boost = self.max_rotate_speed / self.acceleration_rotate_time
        self.boost = self.max_speed / self.acceleration_time
        self.brake = -(self.max_speed / self.braking_time)
        self.image = load_image(self.file_with_image, colorkey=-1)
        self.block = False
        self.last_dt = 0

    def move(self, time, type_="Boost"):
        if self.block:
            self.knockout_animation(time)
            print(self.speed)
            return
        self.last_dt = time
        boost = self.brake if type_ == "Brake" else self.boost
        self.speed = self.speed + boost * time if 0 <= self.speed + boost * time <= self.max_speed else (
            0 if self.speed + boost * time < 0 else self.max_speed)
        self.x_speed = self.speed * sin(radians(self.angle_of_rotation))
        self.y_speed = self.speed * cos(radians(self.angle_of_rotation))
        self.x += self.x_speed * time
        self.y -= self.y_speed * time

    def knockout_animation(self, time):
        boost = self.brake
        self.speed = self.speed + boost * time if 0 <= self.speed + boost * time <= self.max_speed else (
            0 if self.speed + boost * time < 0 else self.max_speed)
        self.x_speed = self.speed * sin(radians((self.angle_of_rotation - 180) % 360))
        self.y_speed = self.speed * cos(radians((self.angle_of_rotation - 180) % 360))
        self.x += self.x_speed * time
        self.y -= self.y_speed * time
        if self.speed == 0:
            self.block = False

    def rotate(self, time, type_):
        boost = self.rotate_boost if type_ == "Right" or (type_ == "Stop" and self.rotate_speed < 0) else (
            -self.rotate_boost if type_ == "Left" or (type_ == "Stop" and self.rotate_speed > 0) else 0)
        if type_ == "Stop" and -1 < self.rotate_speed < 1:
            self.rotate_speed = 0
        else:
            self.rotate_speed = self.rotate_speed + boost * time if (-self.max_rotate_speed <= self.rotate_speed +
                                                                     boost * time <= self.max_rotate_speed) else (
                -self.max_rotate_speed if self.rotate_speed + boost * time < -self.max_rotate_speed
                else self.max_rotate_speed)
        self.angle_of_rotation += self.rotate_speed * time

    def take_damage(self, obj):
        if self.block:
            return
        ship_damage = (self.mass * (self.speed ** 2)) / 2
        ship_damage = ship_damage_x, ship_damage_y = ship_damage * cos(
            radians(self.angle_of_rotation)), ship_damage * sin(radians(self.angle_of_rotation))
        obj_damage = (obj.mass * (obj.speed ** 2)) / 2
        obj_damage = obj_damage_x, obj_damage_y = obj_damage * cos(radians(obj.angle_of_rotation)), obj_damage * sin(
            radians(obj.angle_of_rotation))
        full_damage = ((ship_damage_x + obj_damage_x) ** 2 + (ship_damage_y + obj_damage_y) ** 2) ** 0.5 / 2
        self.deal_damage(full_damage)
        obj.deal_damage(full_damage)

    def deal_damage(self, damage, rotate=False):
        if damage > self.shield:
            self.armor -= damage - self.shield
            self.shield = 0
        else:
            self.shield -= damage
        if self.speed == 0:
            self.speed = self.max_speed + self.height
        self.block = True

    def __str__(self):
        return self.name


class Background:
    def __init__(self):
        self.image = load_image("C:\\Users\\start\\PycharmProjects\\pythonProject1\\data\\background.jpg")
        self.angle_of_rotation = 0


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
