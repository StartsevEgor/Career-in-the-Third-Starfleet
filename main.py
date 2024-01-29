import os
import sys
import pygame
from screeninfo import get_monitors
from game_data import *
from interface import *
import additional_functions

width, height = get_monitors()[0].width, get_monitors()[0].height


def load_map(file):
    objects = []
    with open(file, "r") as file:
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
            elif obj_name == "small asteroid":
                obj = Asteroid("Small asteroid", obj_x, obj_y, asteroid_settings["Small asteroid"])
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


def make_overview_panel():
    data = []
    files_with_images = []
    for object_ in objects:
        if object_ == player_ship:
            continue
        data.append(["", object_, str(object_.speed),
                     str(human_read_format(
                         round(((player_ship.x - object_.x) ** 2 + (player_ship.y - object_.y) ** 2) ** 0.5)))])
        files_with_images.append([object_.file_with_icon_image, None, None, None])
    columns_width = [30, 150, 40, 50]
    table = Table(sum(columns_width), 30 * len(data), width - sum(columns_width), 0, reverse_matrix(data),
                  reverse_matrix(files_with_images), pygame.Color("white"), pygame.Color((0, 0, 0, 255)),
                  interface_sprites, columns_width=columns_width)
    return table


def update_overview_panel():
    data = []
    files_with_images = []
    for object_ in objects:
        if object_ == player_ship:
            continue
        data.append(["", object_, str(object_.speed),
                     str(human_read_format(
                         round(((player_ship.x - object_.x) ** 2 + (player_ship.y - object_.y) ** 2) ** 0.5)))])
        files_with_images.append([object_.file_with_icon_image, None, None, None])
    # overview_panel.data = reverse_matrix(data)
    # overview_panel.files_with_images = reverse_matrix(files_with_images)
    # overview_panel.make(overview_panel.columns_width)
    overview_panel.change(overview_panel.width, 30 * len(data), overview_panel.x, overview_panel.y)
    overview_panel.update_data(reverse_matrix(data), reverse_matrix(files_with_images))


def update_speeds_and_distances_in_overview_panel():
    for i in range(len(overview_panel.data[0])):
        overview_panel.cells[-2][i].text = str(overview_panel.cells[1][i].obj.speed)
        overview_panel.cells[-2][i].update()
        overview_panel.cells[-1][i].text = str(human_read_format(round(((player_ship.x - overview_panel.cells[1][
            i].obj.x) ** 2 + (player_ship.y - overview_panel.cells[1][i].obj.y) ** 2) ** 0.5)))
        overview_panel.cells[-1][i].update()
        overview_panel.update()


def collision_check():
    for i in all_sprites.sprites():
        new_group = all_sprites.copy()
        new_group.remove(i)
        if pygame.sprite.spritecollideany(i, new_group) and not i.obj.knockout_block:
            i.obj.take_damage(pygame.sprite.spritecollideany(i, new_group).obj)


def start_screen():
    intro_text = [["СТАРТ", "Справка"]]
    images = [["", ""]]
    columns_width = [400]
    interface_sprites = pygame.sprite.Group()
    table = Table(sum(columns_width), 200, width / 2 - sum(columns_width) / 2, height / 2 - 100, intro_text, images,
                  pygame.Color("green"), pygame.Color("black"), interface_sprites,
                  text_settings=(None, 50, pygame.Color("green")), columns_width=columns_width)
    fon = pygame.transform.scale(load_image('data/fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button = table.click(pygame.mouse.get_pos())
                    if button and button.text == "СТАРТ":
                        screen_with_levels()
                        return
        screen.blit(fon, (0, 0))
        interface_sprites.draw(screen)
        table.update()
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    intro_text = [["Начать заново"]]
    images = [[""]]
    columns_width = [400]
    interface_sprites = pygame.sprite.Group()
    table = Table(sum(columns_width), 200, width / 2 - sum(columns_width) / 2, height / 2 - 100, intro_text, images,
                  pygame.Color("green"), pygame.Color("black"), interface_sprites,
                  text_settings=(None, 50, pygame.Color("green")), columns_width=columns_width)
    fon = pygame.transform.scale(load_image('data/fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button = table.click(pygame.mouse.get_pos())
                    if button and button.text == "Начать заново":
                        screen_with_levels()
                        return
        screen.blit(fon, (0, 0))
        interface_sprites.draw(screen)
        table.update()
        pygame.display.flip()
        clock.tick(FPS)


def screen_with_levels():
    levels_count = list(range(len(os.listdir("data/Levels"))))
    intro_text = list(map(lambda x: [str(x + 1)], levels_count))
    images = list(map(lambda x: [""], levels_count))
    interface_sprites = pygame.sprite.Group()
    table = Table(width - 1, 300, 0, height / 2 - 150, intro_text, images,
                  pygame.Color("green"), pygame.Color("black"), interface_sprites,
                  text_settings=(None, 100, pygame.Color("green")))
    fon = pygame.transform.scale(load_image('data/fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button = table.click(pygame.mouse.get_pos())
                    if button:
                        main(f"data/Levels/map{button.text}.txt")
                        return
        screen.blit(fon, (0, 0))
        interface_sprites.draw(screen)
        table.update()
        pygame.display.flip()
        clock.tick(FPS)


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
        global overview_panel
        old_width, old_height, old_x, old_y = self.width, self.height, self.x, self.y
        self.width = self.width * approximation_factor
        self.height = self.height * approximation_factor
        self.x = player_ship.x - self.width / 2
        self.y = player_ship.y - self.height / 2
        delete_sprites = []
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
            if sprite.destroy_image_flag:
                delete_sprites.append(sprite)
                objects.remove(sprite.obj)
        if delete_sprites:
            all_sprites.remove(delete_sprites)
            update_overview_panel()


def main(map):
    global objects, main_character_data, all_sprites, interface_sprites, x, x1, player_ship, dt, w_flag, s_flag, \
        a_flag, d_flag, overview_panel, camera, running
    main_character_data = unpacking_txt("data/Main character.txt")
    all_sprites = pygame.sprite.Group()
    background_sprites = pygame.sprite.Group()
    interface_sprites = pygame.sprite.Group()
    objects = load_map(map)
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
    overview_panel = make_overview_panel()
    camera = Camera()
    running = True
    while running:
        if player_ship.destroy_flag:
            running = False
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
                if event.button == 1:
                    print(overview_panel.click(pygame.mouse.get_pos(), get_target=True))
                elif event.button == 4:
                    camera.update(approximation_factor=1.2)
                elif event.button == 5:
                    camera.update(approximation_factor=0.8)
        screen.fill((0, 0, 0))
        update_speeds_and_distances_in_overview_panel()
        collision_check()
        pygame.draw.rect(screen, "white", (1, 1, width - 1, height - 1), 1)
        pygame.draw.rect(screen, "white", (1, 1, width // 2, height), 1)
        pygame.draw.rect(screen, "white", (1, 1, width, height // 2), 1)
        for obj in objects:
            if obj.knockout_block:
                obj.move(dt)
        if w_flag:
            player_ship.move(dt, type_="Boost")
        if s_flag or not w_flag:
            player_ship.move(dt, type_="Brake")
        if a_flag and not d_flag:
            player_ship.rotate(dt, type_="Left")
        if d_flag and not a_flag:
            player_ship.rotate(dt, type_="Right")
        if (not d_flag and not a_flag) or (
                d_flag and a_flag) and player_ship.rotate_speed != 0 and not player_ship.knockout_block:
            player_ship.rotate(dt, type_="Stop")
        background_sprites.draw(screen)
        all_sprites.draw(screen)
        interface_sprites.draw(screen)
        camera.update()
        background_sprites.update()
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000
    end_screen()


pygame.init()
size = width, height
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_screen()
