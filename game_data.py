from math import *
from additional_functions import *

ships_settings = {
    "Civilian ship": {"type": "Истребитель", "width": 50, "height": 55, "mass": 67500,
                      "buy_price": 0,
                      "sell_price": 0,
                      "image": load_image("data/Objects/Ships/Civilian ship/civilian ship.png", colorkey=-1),
                      "icon_image":
                          load_image("data/Objects/Mini images/ship.png", colorkey=-1),
                      "destroy_animation": (load_image("data/explosion.png", colorkey=-1), 8, 6),
                      "level": 1, "energy": 2000000000, "energy_recovery_rate": 8777777, "shield": 1000000000,
                      "armor": 1000000000, "max_speed": 400, "acceleration_time": 1.5, "braking_time": 1,
                      "max_rotate_speed": 120, "acceleration_rotate_time": 0.5}
}
asteroid_settings = {
    "Small asteroid": {"type": "Мелкий астероид", "width": 20, "height": 20, "mass": 20000,
                       "image": load_image("data/Objects/Items/small_asteroid.png", colorkey=-1),
                       "destroy_animation": (load_image("data/explosion.png", colorkey=-1), 8, 6),
                       "icon_image": load_image("data/Objects/Items/small_asteroid.png", colorkey=-1), "shield": 0,
                       "armor": 500000000,
                       "max_speed": 800, "acceleration_time": 0.75, "braking_time": 2, "max_rotate_speed": 240,
                       "acceleration_rotate_time": 0.25}
}
missile_settings = {
    "Laser": {"type": "Лазер", "width": 2, "height": 24, "mass": 1,
              "image": load_image("data/Objects/Items/red_laser.png"),
              "icon_image": load_image("data/Objects/Items/red_laser.png"),
              "destroy_animation": (load_image("data/explosion_electric.png", colorkey=-1), 6, 1), "shield": 0,
              "armor": 0,
              "speed": 800}
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
        self.icon_image = settings["icon_image"]
        self.destroy_animation = cut_sheet(settings["destroy_animation"][0], settings["destroy_animation"][1],
                                           settings["destroy_animation"][2])
        self.level = settings["level"]
        self.energy = settings["energy"]
        self.energy_recovery_rate = settings["energy_recovery_rate"]
        self.damage_energy = 0
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
        self.image = settings["image"]
        self.knockout_block = False
        self.destroy_flag = False
        self.block = False
        self.knockout_angle = 0

    def move(self, time, type_="Brake"):
        if self.block:
            return
        if self.knockout_block:
            self.knockout_animation(time)
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
        self.x_speed = self.speed * sin(radians((self.knockout_angle - 180) % 360))
        self.y_speed = self.speed * cos(radians((self.knockout_angle - 180) % 360))
        self.x += self.x_speed * time
        self.y -= self.y_speed * time
        if self.speed == 0:
            self.knockout_block = False
            self.knockout_angle = 0

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
        if self.knockout_block or obj.destroy_flag or (
                obj.__class__.__name__ == "Missile" and obj.owner == self) or self.speed == 0:
            return
        ship_damage = (self.mass * (self.speed ** 2)) / 2
        ship_damage = ship_damage_x, ship_damage_y = ship_damage * cos(
            radians(self.angle_of_rotation)), ship_damage * sin(radians(self.angle_of_rotation))
        obj_damage = (obj.mass * (obj.speed ** 2)) / 2
        obj_damage = obj_damage_x, obj_damage_y = obj_damage * cos(radians(obj.angle_of_rotation)), obj_damage * sin(
            radians(obj.angle_of_rotation))
        full_damage = ((ship_damage_x + obj_damage_x) ** 2 + (ship_damage_y + obj_damage_y) ** 2) ** 0.5 / 2
        self.deal_damage(full_damage + obj.damage_energy, self.speed + obj.speed, self.angle_of_rotation)
        obj.deal_damage(full_damage, self.speed + obj.speed, (self.angle_of_rotation - 180) % 360)

    def deal_damage(self, damage, knockout_speed, knockout_angle):
        if damage > self.shield:
            self.armor -= damage - self.shield
            self.shield = 0
        else:
            self.shield -= damage
        if self.speed == 0:
            self.speed = self.max_speed + self.height
        self.knockout_block = True
        self.speed = knockout_speed
        self.knockout_angle = knockout_angle
        if self.armor <= 0:
            self.destroy_flag = True
            self.block = True

    def __str__(self):
        return self.name


class Asteroid:
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
        self.image = settings["image"]
        self.icon_image = settings["icon_image"]
        self.destroy_animation = cut_sheet(settings["destroy_animation"][0], settings["destroy_animation"][1],
                                           settings["destroy_animation"][2])
        self.damage_energy = 0
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
        self.knockout_block = False
        self.destroy_flag = False
        self.block = False
        self.knockout_angle = 0

    def move(self, time, type_="Brake"):
        if self.block:
            return
        if self.knockout_block:
            self.knockout_animation(time)
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
        self.x_speed = self.speed * sin(radians((self.knockout_angle - 180) % 360))
        self.y_speed = self.speed * cos(radians((self.knockout_angle - 180) % 360))
        self.x += self.x_speed * time
        self.y -= self.y_speed * time
        if self.speed == 0:
            self.knockout_block = False
            self.knockout_angle = 0

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
        if self.knockout_block or self.destroy_flag or self.speed == 0:
            return
        ship_damage = (self.mass * (self.speed ** 2)) / 2
        ship_damage = ship_damage_x, ship_damage_y = ship_damage * cos(
            radians(self.angle_of_rotation)), ship_damage * sin(radians(self.angle_of_rotation))
        obj_damage = (obj.mass * (obj.speed ** 2)) / 2
        obj_damage = obj_damage_x, obj_damage_y = obj_damage * cos(radians(obj.angle_of_rotation)), obj_damage * sin(
            radians(obj.angle_of_rotation))
        full_damage = ((ship_damage_x + obj_damage_x) ** 2 + (ship_damage_y + obj_damage_y) ** 2) ** 0.5 / 2
        self.deal_damage(full_damage + obj.damage_energy, self.speed + obj.speed, self.angle_of_rotation)
        obj.deal_damage(full_damage, self.speed + obj.speed, (self.angle_of_rotation - 180) % 360)

    def deal_damage(self, damage, knockout_speed, knockout_angle):
        if damage > self.shield:
            self.armor -= damage - self.shield
            self.shield = 0
        else:
            self.shield -= damage
        if self.speed == 0:
            self.speed = self.max_speed + self.height
        self.knockout_block = True
        self.speed = knockout_speed
        self.knockout_angle = knockout_angle
        if self.armor <= 0:
            self.destroy_flag = True
            self.block = True

    def __str__(self):
        return self.name


class Missile:
    def __init__(self, owner, name, x, y, angle_of_rotation, settings):
        super().__init__()
        self.owner = owner
        self.name = name
        self.x, self.y = x, y
        self.angle_of_rotation = angle_of_rotation
        self.speed = 0
        self.x_speed = 0
        self.y_speed = 0
        self.type_ = settings["type"]
        self.width = settings["width"]
        self.height = settings["height"]
        self.mass = settings["mass"]
        self.image = settings["image"]
        self.icon_image = settings["icon_image"]
        self.destroy_animation = cut_sheet(settings["destroy_animation"][0], settings["destroy_animation"][1],
                                           settings["destroy_animation"][2])
        self.damage_energy = 100000000
        self.shield = settings["shield"]
        self.armor = settings["armor"]
        self.speed = settings["speed"]
        self.knockout_block = False
        self.destroy_flag = False
        self.block = False

    def move(self, time):
        if abs(abs((self.owner.x ** 2 + self.owner.y ** 2) ** 0.5) - abs((self.x ** 2 + self.y ** 2) ** 0.5)) > 1000:
            self.deal_damage()
        if self.block:
            return
        self.last_dt = time
        self.x_speed = self.speed * sin(radians(self.angle_of_rotation))
        self.y_speed = self.speed * cos(radians(self.angle_of_rotation))
        self.x += self.x_speed * time
        self.y -= self.y_speed * time

    def take_damage(self, obj):
        if self.destroy_flag or obj == self.owner or self.speed == 0:
            return
        ship_damage = (self.mass * (self.speed ** 2)) / 2
        ship_damage = ship_damage_x, ship_damage_y = ship_damage * cos(
            radians(self.angle_of_rotation)), ship_damage * sin(radians(self.angle_of_rotation))
        obj_damage = (obj.mass * (obj.speed ** 2)) / 2
        obj_damage = obj_damage_x, obj_damage_y = obj_damage * cos(radians(obj.angle_of_rotation)), obj_damage * sin(
            radians(obj.angle_of_rotation))
        full_damage = ((ship_damage_x + obj_damage_x) ** 2 + (ship_damage_y + obj_damage_y) ** 2) ** 0.5 / 2
        self.deal_damage(full_damage, self.speed + obj.speed, self.angle_of_rotation)
        obj.deal_damage(full_damage + self.damage_energy, self.speed + obj.speed, (self.angle_of_rotation - 180) % 360)

    def deal_damage(self, *args):
        self.destroy_flag = True
        self.block = True

    def __str__(self):
        return self.name


class Background:
    def __init__(self):
        self.image = load_image("data\\background.jpg")
        self.angle_of_rotation = 0
