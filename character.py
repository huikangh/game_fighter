import random
from attack import *


class Character:
    def __init__(self, x, y):
        self.x = x                              # x coordinate of object
        self.y = y                              # y coordinate of object
        self.mov_spd = None                     # how much pixel is the object moving
        self.atk = None                         # how much damage is the object's attack
        self.atk_cd = None                      # the cool down period between each attack
        self.cd_counter = 0                     # counter for counting the cool down period
        self.health = None                      # current health of object
        self.max_health = None                  # maximum health of object
        self.char_img = None                    # image for the object
        self.atk_img = None                     # image for the object's attack

    def draw(self, window):
        window.blit(self.char_img, (self.x, self.y))
        self.healthbar(window)

    def attack(self, dx, dy, spd):
        if self.cd_counter == 0:
            new_attack = Attack(self.x, self.y, dx, dy, 0.5*self.atk, spd, self.atk_img)
            if not new_attack.off_screen(WIDTH, HEIGHT):
                pygame.mixer.Sound.play(blast_sound)
            self.cd_counter = 1
            return new_attack
        return None

    def cooldown(self):
        # attack is ready if cd_counter reaches the object's atk_cd
        if self.cd_counter >= self.atk_cd:
            self.cd_counter = 0
        elif self.cd_counter > 0:
            self.cd_counter += 1

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0),
            (self.x, self.y+self.char_img.get_height()+3, self.char_img.get_width(), 3))
        pygame.draw.rect(window, (0,255,0),
            (self.x, self.y+self.char_img.get_height()+3, self.char_img.get_width()*self.health/self.max_health, 3))

    def knocked_back(self, x, y, kb_dist):
        # unit is knocked back towards the opposite direction of (x,y)
        dx = x - self.x
        dy = y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        self.x -= kb_dist * (dx/dist)
        self.y -= kb_dist * (dy/dist)

    def get_width(self):
        return self.char_img.get_width()

    def get_height(self):
        return self.char_img.get_height()


class Hero(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 3
        self.atk = 100
        self.atk_cd = 45
        self.health = 100
        self.max_health = 100
        self.char_img = HIKARI
        self.atk_img = WIND_ARROW
        self.mask = pygame.mask.from_surface(self.char_img)
        self.attacks = []   # a list that stores all the player's attacks

    def draw(self, window):
        window.blit(self.char_img, (self.x, self.y))
        for attack in self.attacks:
            attack.draw(window)
        self.healthbar(window)

    def attack(self, dx, dy, spd):
        if self.cd_counter == 0:
            # adjust the x/y coordinates a bit based on the image size
            x = self.x + (self.get_width()- 15)/2
            y = self.y + (self.get_height()-15)/2
            new_attack = Attack(x, y, dx, dy, self.atk, spd, self.atk_img)
            pygame.mixer.Sound.play(arrow_sound)
            self.attacks.append(new_attack)
            self.cd_counter = 1

    def move_attack(self, objs):
        self.cooldown()
        for attack in self.attacks:
            attack.move()
            if attack.off_screen(WIDTH, HEIGHT):
                self.attacks.remove(attack)
            else:
                # check if the player's attack hit any enemy among all the enemies
                for obj in objs:
                    if attack.collision(obj):
                        obj.health -= attack.dmg
                        obj.knocked_back(self.x, self.y, 0.5*obj.get_width())
                        if obj.health <= 0:
                            objs.remove(obj)
                        if attack in self.attacks: self.attacks.remove(attack)


class EnemyRed(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 2
        self.atk = 40
        self.atk_cd = None
        self.health = 200
        self.max_health = 200
        self.char_img = GOBLIN
        self.atk_img = PD_21_BULLET
        self.mask = pygame.mask.from_surface(self.char_img)

    def chase(self, x, y):
        # move towards the given (x,y) coordinate
        dx = x - self.x
        dy = y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        self.x += self.mov_spd * dx/dist
        self.y += self.mov_spd * dy/dist


class EnemyBlue(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 1
        self.atk = 40
        self.atk_cd = 90
        self.cd_counter = random.randrange(0, self.atk_cd)
        self.health = 100
        self.max_health = 100
        self.char_img = CROW
        self.atk_img = PD_21_BULLET
        self.mask = pygame.mask.from_surface(self.char_img)

    def calc_dxdy(self, x, y):
        # calculate the delta_x and delta_y from unit to target as a value in [0,1] where dx + dy = 1
        dx = x - self.x
        dy = y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        return dx / dist, dy / dist

    def chase(self, x, y):
        # move towards the given (x,y) coordinate
        dx = x - self.x
        dy = y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        self.x += self.mov_spd * dx / dist
        self.y += self.mov_spd * dy / dist


class EnemyBoss(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 1.5
        self.atk = 50
        self.atk_cd = 90
        self.cd_counter = random.randrange(0, self.atk_cd)
        self.health = 2500
        self.max_health = 2500
        self.char_img = TRUE_DEVIL_CAIN
        self.atk_img = MD_21_BULLET
        self.mask = pygame.mask.from_surface(self.char_img)

    def knocked_back(self, x, y, kb_dist):
        # unit is knocked back towards the opposite direction of (x,y)
        dx = x - self.x
        dy = y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        self.x -= kb_dist * (dx/dist) * 0.25
        self.y -= kb_dist * (dy/dist) * 0.25

    def calc_dxdy(self, x, y):
        # calculate the delta_x and delta_y from unit to target as a value in [0,1] where dx + dy = 1
        dx = x - self.x
        dy = y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        return dx/dist, dy/dist

    def chase(self, x, y):
        # move towards the given (x,y) coordinate
        dx = x - self.x
        dy = y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        self.x += self.mov_spd * dx/dist
        self.y += self.mov_spd * dy/dist

    def hoover(self):
        dx = random.random()
        dy = 1 - dx
        # 50/50 to decide whether dx and dy are positive or negative
        if random.random() <= 0.5:
            dx = -dx
        if random.random() <= 0.5:
            dy = -dy
        self.x += self.mov_spd * dx
        self.y += self.mov_spd * dy

    def attack(self, dx, dy, spd):
        # fire multiple attacks in the shape of a fan
        shots = []
        if self.cd_counter == 0:
            angles = [-45, -22.5, 0, 22.5, 45]
            for a in angles:
                angle = a + math.degrees(math.atan(dy/dx))
                new_dx = math.cos(math.radians(angle))
                new_dy = math.sin(math.radians(angle))
                new_dx = -new_dx if dx < 0 else new_dx
                new_dy = -new_dy if dx < 0 else new_dy
                shot = Attack(self.x, self.y, new_dx, new_dy, 0.5*self.atk, spd, self.atk_img)
                shots.append(shot)
            if not shots[2].off_screen(WIDTH, HEIGHT):
                pygame.mixer.Sound.play(laser_sound)
            self.cd_counter = 1
        return shots

