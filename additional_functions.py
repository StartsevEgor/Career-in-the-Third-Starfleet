import os
import sys
import pygame
from screeninfo import get_monitors

FPS = 60
def human_read_format(size):
    values = ["М", "Км", "Мм"]
    count = 0
    while size >= 1000:
        if count + 1 == 3:
            break
        size /= 1000
        count += 1
    return f"{round(size)}{values[count]}"


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
        if colorkey == -1:
            deleted_pixels = list(set(tuple(image.get_at((i, 0))) for i in range(image.get_width())))
            for j in deleted_pixels:
                for x in range(image.get_width()):
                    for y in range(image.get_height()):
                        if image.get_at((x, y)) == j:
                            image.set_at((x, y), (0, 0, 0, 255))
            image.set_colorkey((0, 0, 0, 255))
    else:
        image = image.convert_alpha()
    return image


def reverse_matrix(matrix):
    new_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    return new_matrix


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
    def __init__(self, width, height, x, y, obj, *group):
        super().__init__(*group)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.obj = obj
        self.change()

    def change(self, new_width=None, new_height=None, new_x=None, new_y=None):
        self.x = new_x if new_x else self.x
        self.y = new_y if new_y else self.y
        self.width = new_width if new_width else self.width
        self.height = new_height if new_height else self.height
        self.image = self.obj.image
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.obj.angle_of_rotation % 360)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
