import math
from assets import *


# given two object, check whether their masks collide
def collide(obj1, obj2):
    offset_x = int(obj2.true_x - obj1.true_x)
    offset_y = int(obj2.true_y - obj1.true_y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


class Attack:
    def __init__(self, x, y, dx, dy, dmg, spd, img):
        self.x = x                          # the starting x coordinate of the attack
        self.y = y                          # the starting y coordinate of the attack
        self.dx = dx                        # the percent change in the x direction (dx+dy = 1)
        self.dy = dy                        # the fraction change in the y direction (dx+dy = 1)
        self.dmg = dmg                      # the amount of damage this attack will do
        self.spd = spd                      # how fast the attack will be moving
        self.img = img
        self.true_x = self.x + self.img.get_width()/2
        self.true_y = self.y + self.img.get_height()/2
        self.mask = pygame.mask.from_surface(self.img)
        # if dx is not 0, determine how the attack should rotate to face the target
        if dx > 0:
            self.img = pygame.transform.rotate(img, -90-math.degrees(math.atan(dy/dx)))
        elif dx < 0:
            self.img = pygame.transform.rotate(img, 90-math.degrees(math.atan(dy/dx)))
        elif dx == 0 and dy > 0:
            self.img = pygame.transform.rotate(img, -180)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.dx * self.spd
        self.y += self.dy * self.spd
        self.true_x += self.dx * self.spd
        self.true_y += self.dy * self.spd


    def off_screen(self, width, height):
        return self.true_x < 0 or self.true_x > width or self.true_y < 0 or self.true_y > height

    def collision(self, obj):
        return collide(self, obj)

