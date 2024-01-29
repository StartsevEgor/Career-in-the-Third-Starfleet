import pygame
import sys
import os
from additional_functions import *


class Interface_Sprite(pygame.sprite.Sprite):
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
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.update()

    def change_color(self, new_background_color=None):
        self.background_color = new_background_color if new_background_color else self.background_color
        self.image.fill(self.background_color)


class Cell(Interface_Sprite):
    def __init__(self, lines_color, background_color, width, height, x, y,
                 text_settings=("", None, 50, pygame.Color("black")), image=None, *group):
        super().__init__(width, height, x, y, background_color, group)
        self.lines_color = lines_color
        self.file_with_image = image
        self.obj = text_settings[0]
        self.text = str(text_settings[0])
        self.font = text_settings[1]
        self.text_size = text_settings[2]
        self.text_color = text_settings[3]
        self.update()

    def update(self):
        super().update()
        self.image.fill(self.background_color)
        font = pygame.font.Font(self.font, self.text_size)
        text = font.render(self.text, True, self.text_color)
        self.height = text.get_height() if text.get_height() > self.height else self.height
        text_x = self.width // 2 - text.get_width() // 2
        text_x = 0 if text_x < 0 else text_x
        text_y = self.height // 2 - text.get_height() // 2
        text_y = 0 if text_y < 0 else text_y
        if self.file_with_image:
            image = load_image(self.file_with_image, colorkey=-1)
            if self.width < self.height:
                image_width = self.width
                image_height = image_width * (image.get_height() / image.get_width())
                x = 1
                y = self.height / 2 - image_height / 2
            else:
                image_height = self.height
                image_width = image_height * (image.get_width() / image.get_height())
                x = self.width / 2 - image_width / 2
                y = 1
            image = pygame.transform.scale(image, (image_width - 2, image_height - 2))
            self.image.blit(image, (x, y))
        self.image.blit(text, (text_x, text_y))
        pygame.draw.rect(self.image, self.lines_color, (0, 0, self.width, self.height), 1)


class Table(Interface_Sprite):
    def __init__(self, width, height, x, y, data: list, files_with_images, lines_color, background_color, *group,
                 text_settings=(None, 20, pygame.Color("white")), columns_width=None):
        super().__init__(width, height, x, y, background_color, *group)
        self.cell_sprites = pygame.sprite.Group()
        self.horizontal_border_sprites = pygame.sprite.Group()
        self.vertical_border_sprites = pygame.sprite.Group()
        self.lines_color = lines_color
        self.background_color = background_color
        self.data = data
        self.target = None
        self.highlighting = None
        self.files_with_images = files_with_images
        self.text_settings = text_settings
        self.columns_width = columns_width if columns_width else [self.width / len(self.data)] * len(self.data)
        self.make(columns_width)

    def make(self, columns_width=None):
        self.image.fill(self.background_color)
        self.columns_width = columns_width if columns_width else self.columns_width
        self.row_height = self.height / len(max(self.data, key=lambda x: len(x)))
        self.cells = []
        for col in range(len(self.data)):
            cell_group = []
            for row in range(len(self.data[col])):
                cell_group.append(Cell(self.lines_color, self.background_color, self.columns_width[col] - 1,
                                       self.row_height - 1, sum(self.columns_width[:col]), self.row_height * row,
                                       (self.data[col][row],) + self.text_settings, self.files_with_images[col][row],
                                       self.cell_sprites))
            self.cells.append(cell_group)
        self.cell_sprites.draw(self.image)

    def update(self):
        self.image.fill(self.background_color)
        self.cell_sprites.draw(self.image)

    def update_data(self, new_data, files_with_images):
        self.image.fill(self.background_color)
        self.data = new_data
        self.files_with_images = files_with_images
        self.make()

    def take_aim(self, row, get_target=False):
        if self.highlighting is not None:
            for col in range(len(self.cells)):
                self.cells[col][self.highlighting].change_color(pygame.Color((0, 0, 0)))
                self.cells[col][self.highlighting].update()
        if get_target:
            self.target = (self.cells[1][row], row)
        for col in range(len(self.cells)):
            self.cells[col][row].change_color(pygame.Color((100, 100, 150, 100)))
            self.cells[col][row].update()
            self.highlighting = row

    def click(self, pos, get_target=False):
        pos = (pos[0] - self.x, pos[1] - self.y)
        for col in range(len(self.cells)):
            for row in range(len(self.cells[col])):
                if self.cells[col][row].rect.collidepoint(pos):
                    self.take_aim(row, get_target)
                    return self.cells[col][row]
        return None
