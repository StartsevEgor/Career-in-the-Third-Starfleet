import os
import sys
import pygame
from screeninfo import get_monitors
from game_data import *

# Изображение не получится загрузить
# без предварительной инициализации pygame

pygame.init()
size = width, height = get_monitors()[0].width, get_monitors()[0].height
drawing_range = width * 2.5, height * 2.5
print(size)
screen = pygame.display.set_mode(size)
FPS = 10


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        deleted_pixels = []
        if colorkey == -1:
            deleted_pixels = list(set(tuple(image.get_at((i, 0))) for i in range(image.get_width())))
            for j in deleted_pixels:
                for x in range(image.get_width()):
                    for y in range(image.get_height()):
                        if image.get_at((x, y)) == j:
                            image.set_at((x, y), (0, 0, 0, 255))
            image.set_colorkey((0, 0, 0, 255))
            deleted_pixels = set(deleted_pixels)
            print(deleted_pixels)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                image = sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size))
                image = image.convert()
                image = pygame.transform.scale(image, (400, 300))
                self.frames.append(image)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Standart_Sprite(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, background_color=pygame.Color("black"), *group):
        super().__init__(*group)
        self.background_color = background_color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.width = 0 if self.width < 0 else self.width
        self.height = 0 if self.height < 0 else self.height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.background_color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def change(self, new_width, new_height, new_x, new_y):
        self.width = new_width
        self.height = new_height
        self.x = new_x
        self.y = new_y
        self.rect.x = new_x
        self.rect.y = new_y
        self.rect.width = new_width
        self.rect.height = new_height
        self.update()


class Camera:
    def __init__(self):
        self.center


def terminate():
    pygame.quit()
    sys.exit()


all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)
terminate()
