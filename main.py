import os
import sys
import pygame
from screeninfo import get_monitors
from game_data import *
import additional_functions

width, height = get_monitors()[0].width, get_monitors()[0].height
classes = {"Civilian ship": Civilian_ship}


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
                obj = classes[main_character_data["Main ship"]]("Player ship", obj_x, obj_y, all_sprites)
            elif obj_name == "civilian ship":
                obj = classes["Civilian ship"]("Civilian ship", obj_x, obj_y, all_sprites)

            objects.append(obj)

    return objects


def terminate():
    pygame.quit()
    sys.exit()


class Camera:
    def __init__(self):
        self.width = width
        self.height = height
        self.x = player_ship.x - self.width / 2
        self.y = player_ship.y - self.height / 2
        for obj in objects:
            print(1)
            obj_sprite_width = width * (obj.width / self.width)
            obj_sprite_height = height * (obj.height / self.height)
            obj_sprite_x = obj.x - obj_sprite_width / 2 - self.x
            obj_sprite_y = obj.y - obj_sprite_height / 2 - self.y
            print(obj_sprite_x, obj_sprite_y)
            Standart_Sprite(obj_sprite_width, obj_sprite_height, obj_sprite_x, obj_sprite_y, obj, all_sprites)

    def update(self, new_width=None, new_height=None):
        self.width = new_width if new_width else self.width
        self.height = new_height if new_height else self.height
        self.x = player_ship.x - self.width / 2
        self.y = player_ship.y - self.height / 2
        for sprite in all_sprites.sprites():
            print(1)
            obj_sprite_width = width * (sprite.obj.width / self.width)
            obj_sprite_height = height * (sprite.obj.height / self.height)
            obj_sprite_x = sprite.obj.x - obj_sprite_width - self.x
            obj_sprite_y = sprite.obj.y - obj_sprite_height - self.y
            print(obj_sprite_x, obj_sprite_y)
            sprite.change(new_width=obj_sprite_width, new_height=obj_sprite_height, new_x=obj_sprite_x, new_y=obj_sprite_y)


pygame.init()
size = width, height
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()
main_character_data = unpacking_txt("data/Main character.txt")
all_sprites = pygame.sprite.Group()
objects = load_map()
x = 0
x1 = 5
player_ship = None
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
                player_ship.move(1000 / FPS, type_="Boost")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                camera.update(new_width=camera.width * 1.2, new_height=camera.height * 1.2)
                # obj.sprite.change(new_x=(obj.sprite.start_x - player_ship.sprite.start_x) * 0.2, new_y=(obj.sprite.start_y - player_ship.sprite.start_y) * 0.2)
            elif event.button == 5:
                camera.update(new_width=camera.width * 0.8, new_height=camera.height * 0.8)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, "white", (1, 1, width - 1, height - 1), 1)
    pygame.draw.rect(screen, "white", (1, 1, width // 2, height), 1)
    pygame.draw.rect(screen, "white", (1, 1, width, height // 2), 1)
    # Отрисовка объектов, находящихся в пределах экрана
    x1 *= -1 if x < 0 or x > width else 1
    x += x1
    all_sprites.draw(screen)
    pygame.draw.circle(screen, "red", (x, 250), 20)
    pygame.display.flip()
    clock.tick(FPS)
terminate()
