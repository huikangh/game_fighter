import pygame
from assets import *


# given two object, check whether their masks collide
def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


class Attack:
    def __init__(self, x, y, dir, img):
        self.x = x
        self.y = y
        self.dir = dir
        self.spd = 10
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self):
        if self.dir == "w":
            self.y -= self.spd
        elif self.dir == "s":
            self.y += self.spd
        elif self.dir == "a":
            self.x -= self.spd
        elif self.dir == "d":
            self.x += self.spd

    def off_screen(self, width, height):
        return self.x < 0 or self.x > width or self.y < 0 or self.y > height

    def collision(self, obj):
        return collide(self, obj)