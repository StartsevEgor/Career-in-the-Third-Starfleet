import os
import sys
import pygame
from screeninfo import get_monitors
from game_data import *
import additional_functions


# Изображение не получится загрузить
# без предварительной инициализации pygame


class Camera:
    def __init__(self):
        self.main_character = map_.search("Character 1", "character", accurate_search=True)
        self.main_ship = self.main_character.main_ship
        all_sprites.draw(screen)

def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
size = width, height
print(size)
screen = pygame.display.set_mode(size)
FPS = 20
camera = Camera()
additional_functions.center = camera.main_character.coordinates[0], -camera.main_character.coordinates[1]
camera.main_ship.change(new_approximation_factor=3)
clock = pygame.time.Clock()
x_pos = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 0, 0), (x_pos, 200), 20)
    all_sprites.draw(screen)
    x_pos += 10

    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)
terminate()
