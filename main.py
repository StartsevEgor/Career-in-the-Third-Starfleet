import os
import sys
import pygame
from screeninfo import get_monitors
from game_data import *
from interface import *
import additional_functions

width, height = get_monitors()[0].width, get_monitors()[0].height
print(width, height)


# Изображение не получится загрузить
# без предварительной инициализации pygame


# class Camera:
#     def __init__(self):
#         self.main_character = map_.search("Character 1", "character", accurate_search=True)
#         self.main_ship = self.main_character.main_ship
#         all_sprites.draw(screen)

# Загрузка карты
def load_map():
    objects = []
    with open("data/map.txt", "r") as file:
        for line in file:
            data = line.strip().split(" - ")
            obj_name = data[0]
            obj_coords = data[1].split(";")
            obj_x = int(obj_coords[0])
            obj_y = int(obj_coords[1])

            # Создание объекта на основе его имени
            if obj_name == "player ship":
                obj = Ship("Player ship", obj_x, obj_y, ships_settings[main_character_data["Main ship"]])
            elif obj_name == "civilian ship":
                obj = Ship("Civilian ship", obj_x, obj_y, ships_settings["Civilian ship"])
            objects.append(obj)
    return objects


def terminate():
    pygame.quit()
    sys.exit()
def get_background_size(background):
    if background.obj.image.get_width() > background.obj.image.get_height():
        image_width = width
        image_height = image_width * (background.obj.image.get_height() / background.obj.image.get_width())
        x = 0
        y = height / 2 - image_height / 2
    else:
        image_height = height
        image_width = image_height * (background.obj.image.get_width() / background.obj.image.get_height())
        x = width / 2 - image_width / 2
        y = 0
    return image_width, image_height, x, y
def make_overview_panel(objects_):
    data = []
    for object_ in objects_:
        pass

class Camera:
    def __init__(self):
        self.width = width
        self.height = height
        self.x = player_ship.x - self.width / 2
        self.y = player_ship.y - self.height / 2
        for obj in objects:
            obj_sprite_width = width * (obj.width / self.width)
            obj_sprite_height = height * (obj.height / self.height)
            obj_sprite_x = (obj.x - self.x - obj_sprite_width / 2) / self.width * width
            obj_sprite_y = (obj.y - self.y - obj_sprite_height / 2) / self.height * height
            Standart_Sprite(obj_sprite_width, obj_sprite_height, obj_sprite_x, obj_sprite_y, obj, all_sprites)

    def update(self, approximation_factor=1):
        old_width, old_height, old_x, old_y = self.width, self.height, self.x, self.y
        self.width = self.width * approximation_factor
        self.height = self.height * approximation_factor
        self.x = player_ship.x - self.width / 2
        self.y = player_ship.y - self.height / 2
        for sprite in all_sprites.sprites():
            obj_sprite_width = sprite.width / approximation_factor
            obj_sprite_height = sprite.height / approximation_factor
            obj_sprite_x = (sprite.obj.x - self.x) / self.width * width - obj_sprite_width / 2
            obj_sprite_y = (sprite.obj.y - self.y) / self.height * height - obj_sprite_height / 2
            if sprite.obj == player_ship and (
                    1 > obj_sprite_height or obj_sprite_height > height or 1 > obj_sprite_width or obj_sprite_width > width):
                self.width, self.height, self.x, self.y = old_width, old_height, old_x, old_y
                return
            sprite.change(new_width=obj_sprite_width, new_height=obj_sprite_height, new_x=obj_sprite_x,
                          new_y=obj_sprite_y)


pygame.init()
size = width, height
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()
main_character_data = unpacking_txt("data/Main character.txt")
all_sprites = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()
objects = load_map()
x = 0
x1 = 40
player_ship = None
dt = 1000 / FPS / 1000
w_flag = s_flag = a_flag = d_flag = False
background = Standart_Sprite(width, height, 0, 0, Background(), background_sprites)
size = get_background_size(background)
background.change(new_width=size[0], new_height=size[1], new_x=size[2], new_y=size[3])
for obj in objects:
    if obj.name == "Player ship":
        player_ship = obj
        break
camera = Camera()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_w:
                w_flag = True
            elif event.key == pygame.K_s:
                s_flag = True
            elif event.key == pygame.K_a:
                a_flag = True
            elif event.key == pygame.K_d:
                d_flag = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                w_flag = False
            elif event.key == pygame.K_s:
                s_flag = False
            elif event.key == pygame.K_a:
                a_flag = False
            elif event.key == pygame.K_d:
                d_flag = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                camera.update(approximation_factor=1.2)
            elif event.button == 5:
                camera.update(approximation_factor=0.8)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, "white", (1, 1, width - 1, height - 1), 1)
    pygame.draw.rect(screen, "white", (1, 1, width // 2, height), 1)
    pygame.draw.rect(screen, "white", (1, 1, width, height // 2), 1)
    if w_flag:
        player_ship.move(dt, type_="Boost")
    if s_flag or not w_flag:
        player_ship.move(dt, type_="Brake")
    if a_flag and not d_flag:
        player_ship.rotate(dt, type_="Left")
    if d_flag and not a_flag:
        player_ship.rotate(dt, type_="Right")
    if (not d_flag and not a_flag) or (d_flag and a_flag) and player_ship.rotate_speed != 0:
        player_ship.rotate(dt, type_="Stop")
    x1 *= -1 if x < 0 or x > width else 1
    x += x1
    background_sprites.draw(screen)
    all_sprites.draw(screen)
    pygame.draw.circle(screen, "white", (x, 12), 10, 1)
    camera.update()
    pygame.display.flip()
    dt = clock.tick(FPS) / 1000
terminate()
