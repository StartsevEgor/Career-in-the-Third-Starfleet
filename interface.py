import pygame
import sys
import os

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
FPS = 60
print(type(screen))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


class Cell(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y,
                 text_settings=("Раз, раз, раз, проверка", None, 50, pygame.Color("black")), *group):
        super().__init__(*group)
        self.color = color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text_settings[0]
        self.font = text_settings[1]
        self.text_size = text_settings[2]
        self.text_color = text_settings[3]
        self.update()

    def update(self):
        self.width = 0 if self.width < 0 else self.width
        self.height = 0 if self.height < 0 else self.height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill("white")
        font = pygame.font.Font(self.font, self.text_size)
        text = font.render(self.text, True, self.text_color)
        self.height = text.get_height() if text.get_height() > self.height else self.height
        text_x = self.width // 2 - text.get_width() // 2
        text_x = 0 if text_x < 0 else text_x
        text_y = self.height // 2 - text.get_height() // 2
        text_y = 0 if text_y < 0 else text_y
        self.image.blit(text, (text_x, text_y))
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height), 1)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Border(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, *group):
        super().__init__(*group)
        self.color = color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
    def update(self):
        self.width = 0 if self.width < 0 else self.width
        self.height = 0 if self.height < 0 else self.height
        self.image = pygame.Surface((self.width, self.height))
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height), 1)

class Table(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, data: list, color: pygame.Color, top_row: bool,
                 text_settings=(None, 20, pygame.Color("green"))):
        super().__init__(interface_sprites)
        self.cell_sprites = pygame.sprite.Group()
        self.border_sprites = pygame.sprite.Group()
        self.color = color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.data = data
        self.text_settings = text_settings

interface_sprites = pygame.sprite.Group()
data1 = ["text"]
w1 = h1 = 500
clock = pygame.time.Clock()
cell = Cell(pygame.Color("green"), w1, h1, 50, 50)
# interface_sprites.add(cell)
running = True
flag_rize_w = flag_rize_h = False
flag_reduction_w = flag_reduction_h = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                flag_rize_h = True
            if event.key == pygame.K_d:
                flag_rize_w = True
            if event.key == pygame.K_s:
                flag_reduction_h = True
            if event.key == pygame.K_a:
                flag_reduction_w = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                flag_rize_h = False
            if event.key == pygame.K_d:
                flag_rize_w = False
            if event.key == pygame.K_s:
                flag_reduction_h = False
            if event.key == pygame.K_a:
                flag_reduction_w = False
    if flag_rize_w or flag_reduction_w or flag_rize_h or flag_reduction_h:
        cell.width += (3 if flag_rize_w else 0) + (-3 if flag_reduction_w else 0)
        cell.height += (-3 if flag_rize_h else 0) + (3 if flag_reduction_h else 0)
    screen.fill("black")

    # table = Table(data1, pygame.Color("green"), False)
    # draw(screen)
    interface_sprites.draw(screen)
    interface_sprites.update()
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
