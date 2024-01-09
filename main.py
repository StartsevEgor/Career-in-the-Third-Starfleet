import os
import sys
import pygame
from screeninfo import get_monitors
from game_data import *

# Изображение не получится загрузить
# без предварительной инициализации pygame




def load_image(name, colorkey=None):
    fullname = name
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
    def __init__(self, width, height, x, y, *group, background_color=pygame.Color("black"), file_with_image=None):
        super().__init__(*group)
        self.background_color = background_color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.width = 0 if self.width < 0 else self.width
        self.height = 0 if self.height < 0 else self.height
        if file_with_image:
            print(file_with_image)
            self.image = load_image(file_with_image, colorkey=-1)
        else:
            print(2)
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.background_color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # self.rect.width = self.width
        # self.rect.height = self.height
        # screen.blit(self.image, (0, 0))

    def change(self, new_width, new_height, new_x, new_y):
        self.width = new_width
        self.height = new_height
        self.x = new_x
        self.y = new_y
        self.rect.x = new_x
        self.rect.y = new_y
        self.rect.width = new_width
        self.rect.height = new_height


class Camera:
    def __init__(self):
        self.objects = pygame.sprite.Group()
        self.main_character = map_.search("Character 1", "character", accurate_search=True)
        self.main_ship = self.main_character.main_ship
        self.center = x, y = self.main_character.coordinates[0], -self.main_character.coordinates[1]
        self.x = x - (width / 2)
        self.y = y - (height / 2)
        self.approximation_factor = max([width / self.main_ship.width, height / self.main_ship.height])
        sprite_width, sprite_height = self.main_ship.width * self.approximation_factor, self.main_ship.height * self.approximation_factor
        print(self.main_ship.file_with_image)
        print(type(self.objects))
        sprite = Standart_Sprite(sprite_width, sprite_height, x - (sprite_width / 2) - self.x, y - (sprite_height / 2) - self.y, self.objects, file_with_image=self.main_ship.file_with_image)
        print(1, self.objects.sprites())
        print(sprite.x, sprite.y, sprite.width, sprite.height)
        self.objects.draw(screen)

def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
size = width, height = get_monitors()[0].width, get_monitors()[0].height
print(size)
screen = pygame.display.set_mode(size)
FPS = 10
camera = Camera()
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
    camera.objects.draw(screen)
    x_pos += 1
    pygame.display.flip()
    clock.tick(FPS)
terminate()
