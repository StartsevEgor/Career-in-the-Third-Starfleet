import os
import sys
import pygame
from screeninfo import get_monitors

width, height = get_monitors()[0].width, get_monitors()[0].height
center = x, y = 0, 0


def unpacking_txt(file):
    with open(file, "r", encoding="utf8") as text:
        strings = text.readlines()
    keys = list(filter(lambda string: ":" in string or " - " in string, strings))
    data = {}
    for i in strings:
        if i in keys:
            if ":" in i:
                data[i[:-2]] = []
            elif " - " in i:
                data[i[:i.index(" - ")]] = i[i.index(" - ") + 3:].strip()
        else:
            data[list(data.keys())[-1]].append(i.strip())
    return data


def unpacking_txt_to_map(file):
    data = unpacking_txt(file)
    for i in data.keys():
        new_dict = {}
        for j in data[i]:
            new_dict[j.split("{")[0]] = tuple(map(float, j.split("{")[1][:-1].split(";")))
        data[i] = new_dict
    return data


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


# class AnimatedSprite(pygame.sprite.Sprite):
#     def __init__(self, sheet, columns, rows, x, y):
#         super().__init__(all_sprites)
#         self.frames = []
#         self.cut_sheet(sheet, columns, rows)
#         self.cur_frame = 0
#         self.image = self.frames[self.cur_frame]
#         self.rect = self.rect.move(x, y)
#
#     def cut_sheet(self, sheet, columns, rows):
#         self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
#                                 sheet.get_height() // rows)
#         for j in range(rows):
#             for i in range(columns):
#                 frame_location = (self.rect.w * i, self.rect.h * j)
#                 image = sheet.subsurface(pygame.Rect(
#                     frame_location, self.rect.size))
#                 image = image.convert()
#                 image = pygame.transform.scale(image, (400, 300))
#                 self.frames.append(image)
#
#     def update(self):
#         self.cur_frame = (self.cur_frame + 1) % len(self.frames)
#         self.image = self.frames[self.cur_frame]


class Standart_Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_width, sprite_height, sprite_x, sprite_y, *group, background_color=pygame.Color("black"),
                 file_with_image=None, approximation_factor=1):
        super().__init__(*group)
        self.background_color = background_color
        self.approximation_factor = approximation_factor
        self.width = sprite_width * approximation_factor
        self.height = sprite_height * approximation_factor
        print(2, x, y)
        self.x = sprite_x - x - (sprite_width / 2)
        self.y = sprite_y - y - (sprite_height / 2)
        if file_with_image:
            print(file_with_image)
            self.image = load_image(file_with_image, colorkey=-1)
        else:
            print(2)
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.background_color)
        self.change()

    def change(self, new_width=None, new_height=None, new_x=None, new_y=None, new_approximation_factor=None):
        super().update()
        print(center)
        self.approximation_factor = new_approximation_factor if new_approximation_factor else self.approximation_factor
        self.width = new_width if new_width else self.width
        self.height = new_height if new_height else self.height
        self.width = self.width * self.approximation_factor
        self.height = self.height * self.approximation_factor
        self.x = new_x if new_x else self.x
        self.y = new_y if new_y else self.y
        self.x = self.x - center[0] - (self.width / 2) + 300
        print(self.y, center[1], (self.height / 2))
        self.y = self.y + center[1] + (self.height / 2)
        print(self.x, self.y)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
