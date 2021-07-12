import math
import pygame
from attack import *
from assets import *


class Character:
    def __init__(self, x, y):
        self.x = x                              # x coordinate of object
        self.y = y                              # y coordinate of object
        self.mov_spd = None                     # how much pixel is the object moving
        self.atk_cd = None                      # the cool down period between each attack
        self.cd_counter = 0                     # counter for counting the cool down period
        self.health = None                      # current health of object
        self.max_health = None                  # maximum health of object
        self.char_img = None                    # image for the object
        self.atk_img = None                     # image for the object's attack
        self.attacks = []                       # a list that stores all the object's attacks

    def draw(self, window):
        window.blit(self.char_img, (self.x, self.y))
        for attack in self.attacks:
            attack.draw(window)

    def attack(self, dir):
        if self.cd_counter == 0:
            new_attack = Attack(self.x, self.y, dir, self.atk_img)
            self.attacks.append(new_attack)
            self.cd_counter = 1

    def cooldown(self):
        # attack is ready if cd_counter reaches the object's atk_cd
        if self.cd_counter >= self.atk_cd:
            self.cd_counter = 0
        elif self.cd_counter > 0:
            self.cd_counter += 1

    def get_width(self):
        return self.char_img.get_width()

    def get_height(self):
        return self.char_img.get_height()


class Hero(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 3
        self.atk_cd = 60
        self.health = 100
        self.max_health = 100
        self.char_img = YELLOW_SPACE_SHIP
        self.atk_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.char_img)

    def move_attack(self, objs):
        kills = 0
        self.cooldown()
        for attack in self.attacks:
            attack.move()
            if attack.off_screen(WIDTH, HEIGHT):
                self.attacks.remove(attack)
            else:
                # check if the player's attack hit any enemy among all the enemies
                for obj in objs:
                    if attack.collision(obj):
                        objs.remove(obj)
                        if attack in self.attacks: self.attacks.remove(attack)
                        kills += 1
        return kills


class EnemyRed(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 2
        self.atk_cd = 1
        self.health = 100
        self.max_health = 100
        self.char_img = RED_SPACE_SHIP
        self.atk_img = RED_LASER
        self.mask = pygame.mask.from_surface(self.char_img)

    def chase(self, x, y):
        # move towards the given x,y coordinate
        dx = abs(x-self.x)
        dy = abs(y-self.y)
        dist = math.sqrt(dx*dx + dy*dy)
        dx = self.mov_spd * dx/dist
        dy = self.mov_spd * dy/dist

        if self.x > x:
            self.x -= dx
        elif self.x < x:
            self.x += dx
        if self.y > y:
            self.y -= dy
        elif self.y < y:
            self.y += dy



