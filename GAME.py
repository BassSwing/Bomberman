import pygame
import os
import sys
from random import choice, randint
from math import floor, ceil


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_width = tile_height = 56
tile_image = {'wall': pygame.transform.scale(load_image('wall.png'), (tile_width, tile_height)),
              'empty': pygame.transform.scale(load_image('grass.png'), (tile_width, tile_height)),
              'breaking_wall': pygame.transform.scale(load_image('breaking_wall.png'), (tile_width, tile_height))}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_group, all_sprites)
        self.imagename = tile_type
        self.image = tile_image[tile_type]
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tile_width
        self.rect.y = pos_y * tile_height
        self.rect.w = tile_width
        self.rect.h = tile_height


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bomb_sprites, all_sprites)
        self.images = []
        for i in range(1, 5):
            for j in range(10):
                self.images.append(
                    pygame.transform.scale(load_image("bomb_" + str(i) + ".png"), (tile_width, tile_height)))
        self.x = x
        self.y = y
        self.i = 0
        self.image = self.images[self.i]
        self.rect = self.image.get_rect()
        self.exist = True
        if self.x % 1 == 0.5:
            if direction == "right":
                self.x = ceil(self.x)
            else:
                self.x = floor(self.x)
        else:
            self.x = round(self.x)
        if self.y % 1 == 0.5:
            if direction == "down":
                self.y = ceil(self.y)
            else:
                self.y = floor(self.y)
        else:
            self.y = round(self.y)
        self.rect.x = self.x * tile_width + shift
        self.rect.y = self.y * tile_height
        self.rect.w = tile_width
        self.rect.h = tile_height

    def update(self):
        self.i += 1
        if self.i > 39:
            self.exist = False
            self.kill()
            self.destroy()
            return
        self.image = self.images[self.i]
        self.rect = self.image.get_rect()
        self.rect.x = self.x * tile_width + shift
        self.rect.y = self.y * tile_height

    def destroy(self):
        if level[self.y - 1][self.x] != "#":
            explosions[4] = Explosion(self.x, self.y - 1, "up_burst_1.png")
            if level[self.y - 2][self.x] != "#" and self.y - 2 != -1:
                explosions[8] = Explosion(self.x, self.y - 2, "up_burst_end_1.png")

        if level[self.y + 1][self.x] != "#":
            explosions[2] = Explosion(self.x, self.y + 1, "down_burst_1.png")
            if level[self.y + 2][self.x] != "#" and self.y + 2 != max_y + 1:
                explosions[6] = Explosion(self.x, self.y + 2, "down_burst_end_1.png")

        if level[self.y][self.x - 1] != "#":
            explosions[3] = Explosion(self.x - 1, self.y, "left_burst_1.png")
            if level[self.y][self.x - 2] != "#" and self.x - 2 != -1:
                explosions[7] = Explosion(self.x - 2, self.y, "left_burst_end_1.png")

        if level[self.y][self.x + 1] != "#":
            explosions[1] = Explosion(self.x + 1, self.y, "right_burst_1.png")
            if level[self.y][self.x + 2] != "#" and self.x + 2 != max_x + 1:
                explosions[5] = Explosion(self.x + 2, self.y, "right_burst_end_1.png")
        explosions[0] = Explosion(self.x, self.y, "central_burst_1.png")


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, explode_name):
        super().__init__(exp_sprites, all_sprites)
        self.image = pygame.transform.scale(load_image(explode_name), (tile_width, tile_height))
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width + shift
        self.rect.y = y * tile_height
        self.rect.w = tile_width
        self.rect.h = tile_height
        if level[y][x] == "b":
            level[y][x] = "."
            tilesdict[(x, y)].imagename = "empty"
            tilesdict[(x, y)].image = tile_image["empty"]
        self.countt = 0

    def update(self):
        if self.countt == 7:
            self.kill()
        else:
            self.countt += 1


class BomberMan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_sprite, all_sprites)
        self.cur_up_frame = 0
        self.cur_down_frame = 0
        self.cur_left_frame = 0
        self.cur_right_frame = 0
        self.death_frame = 0
        self.stop_up = pygame.transform.scale(load_image('up_1.png'), (tile_width, tile_height))
        self.stop_down = pygame.transform.scale(load_image('down_1.png'), (tile_width, tile_height))
        self.stop_left = pygame.transform.scale(load_image('left_1.png'), (tile_width, tile_height))
        self.stop_right = pygame.transform.scale(load_image('right_1.png'), (tile_width, tile_height))
        self.up = [pygame.transform.scale(load_image('up_' + str(i) + '.png'), (tile_width, tile_height)) for i in
                   range(2, 8)]
        self.down = [pygame.transform.scale(load_image('down_' + str(i) + '.png'), (tile_width, tile_height)) for i in
                     range(2, 8)]
        self.left = [pygame.transform.scale(load_image('left_' + str(i) + '.png'), (tile_width, tile_height)) for i in
                     range(2, 8)]
        self.right = [pygame.transform.scale(load_image('right_' + str(i) + '.png'), (tile_width, tile_height)) for i in
                      range(2, 8)]
        death = [pygame.transform.scale(load_image('death_bomber_' + str(i) + '.png'), (tile_width, tile_height))\
                    for i in range(1, 6)]

        self.dead = []
        for i in death:
            self.dead.append(i)
            self.dead.append(i)
            self.dead.append(i)

        self.image = self.stop_down
        self.rect = self.image.get_rect()
        self.y, self.x = y, x
        self.rect = self.rect.move(self.x * tile_width, self.y * tile_height)
        self.rect.w = tile_width
        self.rect.h = tile_height

    def update(self):
        if direction == 'down':
            self.cur_down_frame = (self.cur_down_frame + 1) % len(self.down)
            self.image = self.down[self.cur_down_frame]
        if direction == 'up':
            self.cur_up_frame = (self.cur_up_frame + 1) % len(self.up)
            self.image = self.up[self.cur_up_frame]
        if direction == 'left':
            self.cur_left_frame = (self.cur_left_frame + 1) % len(self.left)
            self.image = self.left[self.cur_left_frame]
        if direction == 'right':
            self.cur_right_frame = (self.cur_right_frame + 1) % len(self.right)
            self.image = self.right[self.cur_right_frame]
        if direction == 'death':
            self.death_frame = (self.death_frame + 1) % len(self.dead)
            self.image = self.dead[self.death_frame]
            if self.death_frame == 14:
                self.kill()
                game_end()

    def stop(self):
        if self.image in self.down:
            self.image = self.stop_down
        if self.image in self.up:
            self.image = self.stop_up
        if self.image in self.left:
            self.image = self.stop_left
        if self.image in self.right:
            self.image = self.stop_right

    def walking(self):
        global shift
        if direction == "up":
            if (self.x % 1 == 1 / 8 or self.x % 1 == 2 / 8 or self.x % 1 == 3 / 8) and \
                    level[floor(self.y - 1 / 8)][floor(self.x)] == "." and \
                    level[floor(self.y - 1 / 8)][ceil(self.x)] != ".":
                self.y -= 1 / 8
                rang = (self.x % 1) * tile_width
                shift += rang
                self.rect.x -= rang
                for sprite in all_sprites:
                    sprite.rect.x += rang
                self.x = floor(self.x)
            elif (self.x % 1 == 7 / 8 or self.x % 1 == 5 / 8 or self.x % 1 == 6 / 8) and \
                    level[floor(self.y - 1 / 8)][ceil(self.x)] == "." and \
                    level[floor(self.y - 1 / 8)][floor(self.x)] != ".":
                self.y -= 1 / 8
                rang = (1 - (self.x % 1)) * tile_width
                shift -= rang
                self.rect.x += rang
                for sprite in all_sprites:
                    sprite.rect.x -= rang
                self.x = ceil(self.x)
            elif level[floor(self.y - 1 / 8)][ceil(self.x)] == "." and \
                    level[floor(self.y - 1 / 8)][round(self.x)] == "." and \
                    level[floor(self.y - 1 / 8)][floor(self.x)] == ".":
                self.y -= 1 / 8

        if direction == "down":
            if (self.x % 1 == 1 / 8 or self.x % 1 == 2 / 8 or self.x % 1 == 3 / 8) and \
                    level[ceil(self.y + 1 / 8)][floor(self.x)] == "." and \
                    level[ceil(self.y + 1 / 8)][ceil(self.x)] != ".":
                self.y += 1 / 8
                rang = (self.x % 1) * tile_width
                shift += rang
                self.rect.x -= rang
                for sprite in all_sprites:
                    sprite.rect.x += rang
                self.x = floor(self.x)
            elif (self.x % 1 == 7 / 8 or self.x % 1 == 5 / 8 or self.x % 1 == 6 / 8) and \
                    level[ceil(self.y + 1 / 8)][ceil(self.x)] == "." and \
                    level[ceil(self.y + 1 / 8)][floor(self.x)] != ".":
                self.y += 1 / 8
                rang = (1 - (self.x % 1)) * tile_width
                shift -= rang
                self.rect.x += rang
                for sprite in all_sprites:
                    sprite.rect.x -= rang
                self.x = ceil(self.x)
            elif level[ceil(self.y + 1 / 8)][ceil(self.x)] == "." and \
                    level[ceil(self.y + 1 / 8)][round(self.x)] == "." and \
                    level[ceil(self.y + 1 / 8)][floor(self.x)] == ".":
                self.y += 1 / 8

        if direction == "left":
            if (self.y % 1 == 1 / 8 or self.y % 1 == 2 / 8) and \
                    level[floor(self.y)][floor(self.x - 1 / 8)] == "." and \
                    level[ceil(self.y)][floor(self.x - 1 / 8)] != ".":
                self.x -= 1 / 8
                self.rect.x -= 1 / 8 * tile_width
                shift += 1 / 8 * tile_width
                for sprite in all_sprites:
                    sprite.rect.x += 1 / 8 * tile_width
                self.y = floor(self.y)
            elif (self.y % 1 == 7 / 8 or self.y % 1 == 6 / 8) and \
                    level[ceil(self.y)][floor(self.x - 1 / 8)] == "." and \
                    level[floor(self.y)][floor(self.x - 1 / 8)] != ".":
                self.x -= 1 / 8
                self.rect.x -= 1 / 8 * tile_width
                shift += 1 / 8 * tile_width
                for sprite in all_sprites:
                    sprite.rect.x += 1 / 8 * tile_width
                self.y = ceil(self.y)
            elif level[round(self.y)][floor(self.x - 1 / 8)] == "." and \
                    level[ceil(self.y)][floor(self.x - 1 / 8)] == "." and \
                    level[floor(self.y)][floor(self.x - 1 / 8)] == ".":
                self.x -= 1 / 8
                shift += 1 / 8 * tile_width
                self.rect.x -= 1 / 8 * tile_width
                for sprite in all_sprites:
                    sprite.rect.x += 1 / 8 * tile_width

        if direction == "right":
            if (self.y % 1 == 1 / 8 or self.y % 1 == 2 / 8) and \
                    level[floor(self.y)][ceil(self.x + 1 / 8)] == "." and \
                    level[ceil(self.y)][ceil(self.x + 1 / 8)] != ".":
                self.x += 1 / 8
                shift -= 1 / 8 * tile_width
                self.rect.x += 1 / 8 * tile_width
                for sprite in all_sprites:
                    sprite.rect.x -= 1 / 8 * tile_width
                self.y = floor(self.y)
            elif (self.y % 1 == 7 / 8 or self.y % 1 == 6 / 8) and \
                    level[ceil(self.y)][ceil(self.x + 1 / 8)] == "." and \
                    level[floor(self.y)][ceil(self.x + 1 / 8)] != ".":
                self.x += 1 / 8
                shift -= 1 / 8 * tile_width
                self.rect.x += 1 / 8 * tile_width
                for sprite in all_sprites:
                    sprite.rect.x -= 1 / 8 * tile_width
                self.y = ceil(self.y)
            elif level[round(self.y)][ceil(self.x + 1 / 8)] == "." and \
                    level[ceil(self.y)][ceil(self.x + 1 / 8)] == "." and \
                    level[floor(self.y)][ceil(self.x + 1 / 8)] == ".":
                self.x += 1 / 8
                shift -= 1 / 8 * tile_width
                self.rect.x += 1 / 8 * tile_width
                for sprite in all_sprites:
                    sprite.rect.x -= 1 / 8 * tile_width
        self.rect.y = self.y * tile_width


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(door_sprite, all_sprites)
        self.image = pygame.transform.scale(load_image('door.png'), (tile_width, tile_height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * tile_width, y * tile_height)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x, self.y = x, y
        super().__init__(npc_sprites, all_sprites)
        self.cur_left_frame = 0
        self.cur_right_frame = 0
        self.cur_up_frame = 0
        self.cur_down_frame = 0
        self.death_frame = 0
        self.velocity = 1 / 8
        self.direction = self.get_direction(x, y)

    def update(self):
        if self.direction == 'down':
            self.cur_down_frame = (self.cur_down_frame + 1) % len(self.right)
            self.image = self.right[self.cur_down_frame]
        if self.direction == 'up':
            self.cur_up_frame = (self.cur_up_frame + 1) % len(self.left)
            self.image = self.left[self.cur_up_frame]
        if self.direction == 'left':
            self.cur_left_frame = (self.cur_left_frame + 1) % len(self.left)
            self.image = self.left[self.cur_left_frame]
        if self.direction == 'right':
            self.cur_right_frame = (self.cur_right_frame + 1) % len(self.right)
            self.image = self.right[self.cur_right_frame]
        if self.direction == 'death':
            self.death_frame = (self.death_frame + 1) % len(self.dead)
            self.image = self.dead[self.death_frame]
            if self.death_frame == 7:
                self.kill()
                global score
                if type(self) is Potato:
                    score += 10
                elif type(self) is Onion:
                    score += 20
                elif type(self) is Barrel:
                    score += 30
                else:
                    score += 70
                del enemies[enemies.index(self)]
                updating_amount()

    def stop(self):
        self.image = self.stopped

    def get_direction(self, x, y):
        available_directions = []
        if bomb_exist:
            bombx = bomb.x
            bomby = bomb.y
        if level[y + 1][x] == ".":
            if bomb_exist:
                if y + 1 != bomby or x != bombx:
                    available_directions.append("down")
            else:
                available_directions.append("down")
        if level[y - 1][x] == ".":
            if bomb_exist:
                if y - 1 != bomby or x != bombx:
                    available_directions.append("up")
            else:
                available_directions.append("up")
        if level[y][x + 1] == ".":
            if bomb_exist:
                if y != bomby or x + 1 != bombx:
                    available_directions.append("right")
            else:
                available_directions.append("right")
        if level[y][x - 1] == ".":
            if bomb_exist:
                if y != bomby or x - 1 != bombx:
                    available_directions.append("left")
            else:
                available_directions.append("left")
        if len(available_directions) != 0:
            return choice(available_directions)
        else:
            return None

    def walking(self):
        if self.x % 1 == 0 and self.y % 1 == 0 and self.direction != "death":
            self.direction = self.get_direction(int(self.x), int(self.y))
        if self.direction == "up":
            self.y -= self.velocity

        if self.direction == "down":
            self.y += self.velocity

        if self.direction == "left":
            self.x -= self.velocity
            self.rect.x -= self.velocity * tile_height

        if self.direction == "right":
            self.x += self.velocity
            self.rect.x += self.velocity * tile_height
        self.rect.y = self.y * tile_width


class Onion(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity = 1 / 4
        self.stopped = pygame.transform.scale(load_image('onion_left_1.png'), (tile_width, tile_height))
        self.death = [pygame.transform.scale(load_image('onion_7.png'), (tile_width, tile_height))
                      for i in range(1, 5)]
        self.dead = [pygame.transform.scale(load_image('death_' + str(i) + '.png'), (tile_width, tile_height))
                     for i in range(1, 5)]

        self.dead = self.death + self.dead
        self.left = [pygame.transform.scale(load_image('onion_left_' + str(i) + '.png'), (tile_width, tile_height)) for
                     i in
                     range(1, 4)]
        self.right = [pygame.transform.scale(load_image('onion_right_' + str(i) + '.png'), (tile_width, tile_height))
                      for i in
                      range(1, 4)]
        self.image = self.stopped
        self.rect = self.image.get_rect()
        self.y, self.x = y, x
        self.rect = self.rect.move(self.x * tile_width, self.y * tile_height)
        self.rect.w = tile_width
        self.rect.h = tile_height


class Potato(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.death = [pygame.transform.scale(load_image('potato_death.png'), (tile_width, tile_height))
                      for i in range(1, 5)]
        self.dead = [pygame.transform.scale(load_image('death_' + str(i) + '.png'), (tile_width, tile_height))
                     for i in range(1, 5)]

        self.dead = self.death + self.dead

        self.stopped = pygame.transform.scale(load_image('potato_left_1.png'), (tile_width, tile_height))

        self.left = [pygame.transform.scale(load_image('potato_left_' + str(i) + '.png'), (tile_width, tile_height))
                     for i in
                     range(1, 4)]
        self.right = [pygame.transform.scale(load_image('potato_right_' + str(i) + '.png'), (tile_width, tile_height)
                                             ) for i in
                      range(1, 4)]
        self.image = self.stopped
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(self.x * tile_width, self.y * tile_height)
        self.rect.w = tile_width
        self.rect.h = tile_height


class Barrel(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.death = [pygame.transform.scale(load_image('round_death.png'), (tile_width, tile_height))
                      for i in range(1, 5)]

        self.dead = [pygame.transform.scale(load_image('death_' + str(i) + '.png'), (tile_width, tile_height))
                     for i in range(1, 5)]

        self.dead = self.death + self.dead

        self.stopped = pygame.transform.scale(load_image('round_left_1.png'), (tile_width, tile_height))

        self.left = [pygame.transform.scale(load_image('round_left_' + str(i) + '.png'), (tile_width, tile_height))
                     for i in
                     range(1, 4)]
        self.right = [pygame.transform.scale(load_image('round_right_' + str(i) + '.png'), (tile_width, tile_height)
                                             ) for i in
                      range(1, 4)]

        self.image = self.stopped
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(self.x * tile_width, self.y * tile_height)

        self.rect.w = tile_width
        self.rect.h = tile_height

    def get_direction(self, x, y):
        available_directions = []
        if bomb_exist:
            bombx = bomb.x
            bomby = bomb.y
        if level[y + 1][x] != "#":
            if bomb_exist:
                if y + 1 != bomby or x != bombx:
                    available_directions.append("down")
            else:
                available_directions.append("down")
        if level[y - 1][x] != "#":
            if bomb_exist:
                if y - 1 != bomby or x != bombx:
                    available_directions.append("up")
            else:
                available_directions.append("up")
        if level[y][x + 1] != "#":
            if bomb_exist:
                if y != bomby or x + 1 != bombx:
                    available_directions.append("right")
            else:
                available_directions.append("right")
        if level[y][x - 1] != "#":
            if bomb_exist:
                if y != bomby or x - 1 != bombx:
                    available_directions.append("left")
            else:
                available_directions.append("left")
        if len(available_directions) != 0:
            return choice(available_directions)
        else:
            return None


class Coin(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity = 1 / 4
        self.stopped = pygame.transform.scale(load_image('onion_left_1.png'), (tile_width, tile_height))
        self.death = [pygame.transform.scale(load_image('coin_death.png'), (tile_width, tile_height))
                      for i in range(1, 5)]
        self.dead = [pygame.transform.scale(load_image('death_' + str(i) + '.png'), (tile_width, tile_height))
                     for i in range(1, 5)]

        self.dead = self.death + self.dead
        self.left = [pygame.transform.scale(load_image('coin_left_' + str(i) + '.png'), (tile_width, tile_height)) for
                     i in
                     range(1, 4)]
        self.right = [pygame.transform.scale(load_image('coin_right_' + str(i) + '.png'), (tile_width, tile_height))
                      for i in
                      range(1, 4)]
        self.image = self.stopped
        self.rect = self.image.get_rect()
        self.y, self.x = y, x
        self.rect = self.rect.move(self.x * tile_width, self.y * tile_height)
        self.rect.w = tile_width
        self.rect.h = tile_height

    def get_direction(self, x, y):
        available_directions = []
        if y + 1 != 12:
            available_directions.append("down")
        if y - 1 != 0:
            available_directions.append("up")
        if x + 1 != 42:
            available_directions.append("right")
        if x - 1 != 0:
            available_directions.append("left")
        if len(available_directions) != 0:
            return choice(available_directions)
        else:
            return None


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, givenscreen, outline=None):
        if outline:
            pygame.draw.rect(givenscreen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(givenscreen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('TimesNewRoman', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            givenscreen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def spawn_coins():
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                if x != 0 and x != 42:
                    if y != 0 and y != 12:
                        enemies.append(Coin(x, y))


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    coords = []
    tiles = []
    new_player = None
    enemies = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                coords.append((x, y))
                tiles.append(Tile('empty', x, y))
            elif level[y][x] == '#':
                coords.append((x, y))
                tiles.append(Tile('wall', x, y))
            elif level[y][x] == 'b':
                ch = choice([1, 2, 3, 4, 5])
                if ch == 3:
                    tiles.append(Tile('breaking_wall', x, y))
                else:
                    level[y][x] = "."
                    tiles.append(Tile('empty', x, y))
                coords.append((x, y))
            elif level[y][x] == '@':
                coords.append((x, y))
                tiles.append(Tile('empty', x, y))
                new_player = BomberMan(x, y)
                level[y][x] = '.'
            elif level[y][x] == 'O':
                coords.append((x, y))
                tiles.append(Tile('empty', x, y))
                level[y][x] = '.'
                enemies.append(Onion(x, y))
            elif level[y][x] == 'B':
                coords.append((x, y))
                tiles.append(Tile('empty', x, y))
                level[y][x] = '.'
                enemies.append(Barrel(x, y))
            elif level[y][x] == 'P':
                coords.append((x, y))
                tiles.append(Tile('empty', x, y))
                level[y][x] = '.'
                enemies.append(Potato(x, y))

    tilesd = dict(zip(coords, tiles))
    return new_player, enemies, tilesd


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (1000, 724))
    screen.blit((fon), (0, 0))
    startButton = Button((255, 255, 255), 350, 300, 250, 100, "START")

    run = True
    while run:
        startButton.draw(screen, (0, 0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.isOver(pos):
                    screen.fill((0, 0, 0))
                    run = False

            if event.type == pygame.MOUSEMOTION:
                if startButton.isOver(pos):
                    startButton.color = (200, 200, 200)
                else:
                    startButton.color = (255, 255, 255)


def level_animating():
    inscription = pygame.sprite.Sprite(inscription_sprite)
    inscription.image = pygame.transform.scale(load_image("level_" + str(number) + ".png"), (800, 500))
    inscription.rect = inscription.image.get_rect()
    inscription.rect.x = -800
    inscription.rect.y = 125
    while inscription.rect.x != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        screen.fill((0, 0, 0))
        inscription.rect.x += 20
        inscription_sprite.draw(screen)
        pygame.time.delay(15)
        pygame.display.flip()
    pygame.time.delay(300)


def level_generating():
    global shift, bomb_exist, explosions, direction, color, level, max_y, max_x, player, enemies, tilesdict, door, running, all_sprites, door_sprite, \
        player_sprite, npc_sprites, exp_sprites, tile_group, bomb_sprites, enemy_sprites, inscription_sprite, T, start_ticks
    inscription_sprite = pygame.sprite.Group()
    level_animating()
    all_sprites = pygame.sprite.Group()
    door_sprite = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    npc_sprites = pygame.sprite.Group()
    exp_sprites = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    bomb_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    shift = 0
    T = 245
    start_ticks = pygame.time.get_ticks()
    bomb_exist = False
    explosions = [None, None, None, None, None, None, None, None, None]
    direction = "right"
    color = (100, 100, 100)

    pygame.display.set_caption('Bomberman')
    size = width, height = 1000, 725
    screen = pygame.display.set_mode(size)
    screen.fill((100, 100, 100))

    level = load_level("map" + str(number) + ".txt")
    max_y = len(level)
    max_x = len(level[0])
    player, enemies, tilesdict = generate_level(level)
    door = Door(1, 1)
    updating_amount()


def game_end():
    pygame.mouse.set_visible(True)
    global number
    fon = pygame.transform.scale(load_image('game_over_picture.jpg'), (1000, 725))
    screen.blit((fon), (0, 0))
    restartButton = Button((255, 255, 255), 600, 500, 250, 100, "YES")
    quitButton = Button((255, 255, 255), 140, 500, 250, 100, "NO")
    scores()

    run = True
    while run:
        restartButton.draw(screen, (0, 0, 0))
        quitButton.draw(screen, (0, 0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restartButton.isOver(pos):
                    screen.fill((0, 0, 0))
                    run = False
                    number = 1
                    level_generating()
                if quitButton.isOver(pos):
                    screen.fill((0, 0, 0))

            if event.type == pygame.MOUSEMOTION:
                if restartButton.isOver(pos):
                    restartButton.color = (200, 200, 200)
                else:
                    restartButton.color = (255, 255, 255)

                if quitButton.isOver(pos):
                    quitButton.color = (200, 200, 200)
                else:
                    quitButton.color = (255, 255, 255)


def updating_amount():
    global inscription_sprite
    inscription_sprite = pygame.sprite.Group()
    inscription = pygame.sprite.Sprite(inscription_sprite)
    inscription.image = pygame.transform.scale(load_image("Left.png"), (200, 40))
    inscription.rect = inscription.image.get_rect()
    inscription.rect.x = 8
    inscription.rect.y = 8
    nums = str(len(enemies))
    x_n = 230
    for x in nums:
        inscription = pygame.sprite.Sprite(inscription_sprite)
        inscription.image = pygame.transform.scale(load_image(x + ".png"), (30, 40))
        inscription.rect = inscription.image.get_rect()
        inscription.rect.x = x_n
        inscription.rect.y = 8
        x_n += 40
    inscriptiontime = pygame.sprite.Sprite(inscription_sprite)
    inscriptiontime.image = pygame.transform.scale(load_image("time.png"), (200, 40))
    inscriptiontime.rect = inscriptiontime.image.get_rect()
    inscriptiontime.rect.x = 400
    inscriptiontime.rect.y = 8


def scores():
    print(score)


def timer(T):
    global time_sprite, start_ticks
    x_t = 620
    time_sprite = pygame.sprite.Group()
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000

    if T - seconds <= 0:
        spawn_coins()
        zeroT()
        zeroimage = pygame.sprite.Sprite(time_sprite)
        zeroimage.image = pygame.transform.scale(load_image('0.png'), (30, 40))
        zeroimage.rect = zeroimage.image.get_rect()
        zeroimage.rect.x = 600
        zeroimage.rect.y = 8
        return

    for x in str(T - seconds):
        second = pygame.sprite.Sprite(time_sprite)
        second.image = pygame.transform.scale(load_image(x + '.png'), (30, 40))
        second.rect = second.image.get_rect()
        second.rect.x = x_t
        second.rect.y = 8
        x_t += 35


def zeroT():
    global T
    T = 0


if __name__ == '__main__':
    pygame.init()

    running = True
    score = 0
    number = 1
    inscription_sprite = pygame.sprite.Group()
    enemies = []
    pygame.display.set_caption('Bomberman')
    size = width, height = 1000, 725
    screen = pygame.display.set_mode(size)

    start_screen()

    screen.fill((0, 0, 0))
    pygame.display.update()

    level_generating()

    screen.fill((100, 100, 100))
    pygame.mouse.set_visible(False)

    while running:
        if T != 0:
            timer(T)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if bomb_exist == False:
                        if score - 5 > 0:
                            score -= 5
                        else:
                            score = 0
                        bomb = Bomb(player.x, player.y)
                        bomb_exist = True
        if pygame.key.get_pressed()[pygame.K_UP]:
            if direction != "death":
                direction = 'up'
                moving = True

        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            if direction != "death":
                direction = 'down'
                moving = True

        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            if direction != "death":
                direction = 'right'
                moving = True

        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            if direction != "death":
                direction = 'left'
                moving = True

        else:
            moving = False

        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                direction = 'death'
                number = 1

        screen.fill(color)
        if moving:
            player.update()
            player.walking()
        else:
            player.stop()
        if direction == "death":
            player.update()
        if bomb_exist:
            if bomb.exist is False:
                bomb_exist = False
            else:
                bomb.update()

        for explosion in explosions:
            if explosion is not None:
                for enemy in enemies:
                    if pygame.sprite.collide_rect(enemy, explosion) and explosion.countt != 7:
                        enemy.direction = "death"
                if pygame.sprite.collide_rect(player, explosion) and explosion.countt != 7:
                    direction = "death"
                    moving = False
                    number = 1
                explosion.update()

        for enemy in enemies:
            enemy.update()
            enemy.walking()

        if len(enemies) == 0:
            if player.x == 1 and player.y == 1:
                number += 1
                screen.fill((0, 0, 0))
                if number == 4:
                    game_end()
                else:
                    level_generating()
                continue
            color = (0, 100, 0)

        tile_group.draw(screen)
        door_sprite.draw(screen)
        player_sprite.draw(screen)
        bomb_sprites.draw(screen)
        exp_sprites.draw(screen)
        npc_sprites.draw(screen)
        time_sprite.draw(screen)
        inscription_sprite.draw(screen)
        pygame.display.flip()
        pygame.time.delay(75)