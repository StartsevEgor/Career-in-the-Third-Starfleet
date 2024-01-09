import pygame
import sys
import os

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
FPS = 60


def load_image(name, colorkey=None):
    fullname = name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


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


class Cell(Standart_Sprite):
    def __init__(self, lines_color, background_color, width, height, x, y,
                 text_settings=("", None, 50, pygame.Color("black")), *group):
        super().__init__(width, height, x, y, background_color, group)
        self.lines_color = lines_color
        self.text = text_settings[0]
        self.font = text_settings[1]
        self.text_size = text_settings[2]
        self.text_color = text_settings[3]
        # self.surface = surface
        self.update()

    def update(self):
        super().update()
        font = pygame.font.Font(self.font, self.text_size)
        text = font.render(self.text, True, self.text_color)
        self.height = text.get_height() if text.get_height() > self.height else self.height
        text_x = self.width // 2 - text.get_width() // 2
        text_x = 0 if text_x < 0 else text_x
        text_y = self.height // 2 - text.get_height() // 2
        text_y = 0 if text_y < 0 else text_y
        self.image.blit(text, (text_x, text_y))
        pygame.draw.rect(self.image, self.lines_color, (0, 0, self.width, self.height), 1)
        # self.surface.blit(self.image, (self.x, self.y))


class Border(Standart_Sprite):
    def __init__(self, lines_color, width, height, x, y, *group):
        super().__init__(width, height, x, y, pygame.Color("black"), group)
        self.lines_color = lines_color
        # self.surface = surface
        self.update()

    def update(self):
        super().update()
        pygame.draw.rect(self.image, self.lines_color, (0, 0, self.width, self.height), 1)
        # self.surface.blit(self.image, (self.x, self.y))


class Table(Standart_Sprite):
    def __init__(self, width, height, x, y, data: list, lines_color, background_color,
                 text_settings=(None, 20, pygame.Color("green"))):
        super().__init__(width, height, x, y, background_color, interface_sprites)
        self.cell_sprites = pygame.sprite.Group()
        self.horizontal_border_sprites = pygame.sprite.Group()
        self.vertical_border_sprites = pygame.sprite.Group()
        self.lines_color = lines_color
        self.background_color = background_color
        self.data = data
        self.text_settings = text_settings
        self.make()

    def make(self):
        self.columns_width = [self.width / len(self.data)] * len(self.data)
        self.row_height = self.height / len(max(self.data, key=lambda x: len(x)))
        self.upper_border = Border(self.lines_color, self.width, 1, 0, 0, self.horizontal_border_sprites)
        self.right_border = Border(self.lines_color, 1, self.height, self.width, 0,
                                   self.vertical_border_sprites)
        self.lower_border = Border(self.lines_color, self.width, 1, 0, self.height - 1,
                                   self.horizontal_border_sprites)
        self.left_border = Border(self.lines_color, 1, self.height, 0, 0, self.vertical_border_sprites)
        for i in range(len(self.data) - 1):
            x = sum(self.columns_width[:i + 1])
            Border(self.lines_color, 0, self.height, x, 0, self.vertical_border_sprites)
        for col in range(len(self.data)):
            for row in range(len(self.data[col])):
                Cell(self.lines_color, self.background_color, self.columns_width[col] - 1,
                     self.row_height - 1, sum(self.columns_width[:col]), self.row_height * row,
                     (self.data[col][row],) + self.text_settings, self.cell_sprites)
        self.vertical_border_sprites.draw(self.image)
        self.horizontal_border_sprites.draw(self.image)
        self.cell_sprites.draw(self.image)

    def update_size(self, old_mouse_pos, new_mouse_pos, border, is_vertical):
        super().update()
        if is_vertical:
            pass
        else:
            new_x = self.x
            new_width = self.width
            new_y = new_mouse_pos[1] if border == self.upper_border else self.y
            new_height = self.height + (new_mouse_pos[1] - old_mouse_pos[1])
        add_to_width = (new_width - self.width) / len(self.columns_width)
        super().change(new_width, new_height, new_x, new_y)
        self.columns_width = list(map(lambda x: x + add_to_width, self.columns_width))
        self.row_height = self.height / len(max(self.data, key=lambda x: len(x)))
        self.upper_border.change(self.width, 1, 0, 0)
        self.right_border.change(1, self.height, self.width, 0)
        self.lower_border.change(self.width, 1, 0, self.height - 1)
        self.left_border.change(1, self.height, 0, 0)
        for i in range(len(self.data) - 1):
            x = sum(self.columns_width[:i + 1])
            border = self.vertical_border_sprites.sprites()[2:][i]
            border.change(0, self.height, x, 0)
        for col in range(len(self.data)):
            for row in range(len(self.data[col])):
                cell = self.cell_sprites.sprites()[(col + 1) * (row + 1) - 1]
                cell.change(self.columns_width[col] - 1, self.row_height - 1, sum(self.columns_width[:col]),
                            self.row_height * row)
    def update_data(self):
        pass
    def click(self, pos):
        pos = (pos[0] - self.x, pos[1] - self.y)
        for border in self.horizontal_border_sprites:
            print(border.rect.collidepoint(pos), (border.rect.x, border.rect.y), pos)
            if border.rect.collidepoint(pos):
                print(1)
                return Border, border, False
        return None

interface_sprites = pygame.sprite.Group()
data1 = [["text3", "text1"], ["text2", "text4"]]
w1 = h1 = 500
clock = pygame.time.Clock()
table = Table(300, 200, 50, 50, data1, pygame.Color("white"), pygame.Color("black"), (None, 40, pygame.Color("white")))
running = True
click_to_table_flag = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if table.rect.collidepoint(pygame.mouse.get_pos()):
                print(1)
                answer = table.click(pygame.mouse.get_pos())
                if answer:
                    print(2)
                    click_to_table_flag = True
                    type_, sprite, is_vertical = answer
                    old_mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            if click_to_table_flag:
                print(1)
                if type_ == Border:
                    table.update_size(old_mouse_pos, pygame.mouse.get_pos(), sprite, is_vertical)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            click_to_table_flag = False
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.KEYUP:
            pass
    screen.fill("black")
    interface_sprites.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
