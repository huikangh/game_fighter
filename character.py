import math
import pygame
from assets import *


class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mov_spd = None
        self.atk_spd = None
        self.health = None
        self.max_health = None
        self.char_img = None
        self.atk_img = None

    def draw(self, window):
        window.blit(self.char_img, (self.x, self.y))

    def get_width(self):
        return self.char_img.get_width()

    def get_height(self):
        return self.char_img.get_height()


class Hero(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 3
        self.atk_spd = 1
        self.health = 100
        self.max_health = 100
        self.char_img = YELLOW_SPACE_SHIP
        self.atk_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.char_img)


class EnemyRed(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 1
        self.atk_spd = 1
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



