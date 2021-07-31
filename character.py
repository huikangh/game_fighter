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
        self.true_x = None                      # the x coordinate of the center of the image
        self.true_y = None                      # the y coordinate of the center of the image

    def draw(self, window):
        window.blit(self.char_img, (self.x, self.y))
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0),
            (self.x, self.y-3, self.char_img.get_width(), 3))
        pygame.draw.rect(window, (0,255,0),
            (self.x, self.y-3, self.char_img.get_width()*self.health/self.max_health, 3))

    def knocked_back(self, x, y, kb_dist):
        # unit is knocked back towards the opposite direction of (x,y)
        dx = x - self.true_x
        dy = y - self.true_y
        dist = math.sqrt(dx*dx + dy*dy)
        self.x -= kb_dist * (dx/dist)
        self.y -= kb_dist * (dy/dist)
        self.true_x -= kb_dist * (dx/dist)
        self.true_y -= kb_dist * (dy/dist)

    def get_width(self):
        return self.char_img.get_width()

    def get_height(self):
        return self.char_img.get_height()



class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 2
        self.atk = 40
        self.health = 200
        self.max_health = 200
        self.char_img = GOBLIN
        self.facing = "left"
        self.atk_img = PD_21_BULLET
        self.true_x = self.x + self.get_width()/2
        self.true_y = self.y + self.get_height()/2
        self.mask = pygame.mask.from_surface(self.char_img)

    def calc_dxdy(self, x, y):
        # calculate the delta_x and delta_y from unit to target as a value in [0,1] where dx + dy = 1
        dx = x - self.true_x
        dy = y - self.true_y
        dist = math.sqrt(dx * dx + dy * dy)
        return dx / dist, dy / dist

    def chase(self, x, y):
        # move towards the given (x,y) coordinate
        dx = x - self.true_x
        dy = y - self.true_y
        dist = math.sqrt(dx*dx + dy*dy)
        self.x += self.mov_spd * dx/dist
        self.y += self.mov_spd * dy/dist
        self.true_x += self.mov_spd * dx/dist
        self.true_y += self.mov_spd * dy/dist
        # adjust which way the character will face
        if self.facing == "left" and dx < 0:
            self.facing = "right"
            self.char_img = pygame.transform.flip(self.char_img, True, False)
        elif self.facing == "right" and dx > 0:
            self.facing = "left"
            self.char_img = pygame.transform.flip(self.char_img, True, False)



class EnemyRanged(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 1
        self.atk = 40
        self.atk_cd = 90
        self.cd_counter = random.randrange(0, self.atk_cd)
        self.health = 100
        self.max_health = 100
        self.char_img = CROW
        self.facing = "left"
        self.atk_img = PD_21_BULLET
        self.true_x = self.x + self.get_width()/2
        self.true_y = self.y + self.get_height()/2
        self.mask = pygame.mask.from_surface(self.char_img)

    def cooldown(self):
        # attack is ready if cd_counter reaches the object's atk_cd
        if self.cd_counter >= self.atk_cd:
            self.cd_counter = 0
        elif self.cd_counter > 0:
            self.cd_counter += 1

    def attack(self, dx, dy, spd):
        # adjust the x/y coordinates a bit based on the atk_img size (-7.5)
        if self.cd_counter == 0:
            new_attack = Attack(self.true_x-7.5, self.true_y-7.5, dx, dy, 0.5*self.atk, spd, self.atk_img)
            if not new_attack.off_screen(WIDTH, HEIGHT):
                pygame.mixer.Sound.play(blast_sound)
            self.cd_counter = 1
            return new_attack
        return None



class EnemyBoss(EnemyRanged):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 1
        self.atk = 50
        self.atk_cd = 90
        self.cd_counter = random.randrange(0, self.atk_cd)
        self.health = 2500
        self.max_health = 2500
        self.char_img = TRUE_DEVIL_CAIN
        self.facing = "left"
        self.atk_img = MD_21_BULLET
        self.true_x = self.x + self.get_width()/2
        self.true_y = self.y + self.get_height()/2
        self.mask = pygame.mask.from_surface(self.char_img)

    def knocked_back(self, x, y, kb_dist):
        # unit is knocked back towards the opposite direction of (x,y)
        dx = x - self.true_x
        dy = y - self.true_y
        dist = math.sqrt(dx*dx + dy*dy)
        self.x -= kb_dist * (dx/dist) * 0.25
        self.y -= kb_dist * (dy/dist) * 0.25
        self.true_x -= kb_dist * (dx / dist) * 0.25
        self.true_y -= kb_dist * (dy / dist) * 0.25

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
                shot = Attack(self.true_x, self.true_y, new_dx, new_dy, 0.5*self.atk, spd, self.atk_img)
                shots.append(shot)
            if not shots[2].off_screen(WIDTH, HEIGHT):
                pygame.mixer.Sound.play(fire_sound)
            self.cd_counter = 1
        return shots



class Hero(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mov_spd = 3
        self.atk = 100
        self.atk_cd = 45
        self.cd_counter = 1
        self.health = 100
        self.max_health = 100
        self.char_img = HIKARI
        self.atk_img = WIND_ARROW
        self.true_x = self.x + self.get_width()/2
        self.true_y = self.y + self.get_height()/2
        self.mask = pygame.mask.from_surface(self.char_img)
        self.attacks = []   # a list that stores all the player's attacks

    def draw(self, window):
        window.blit(self.char_img, (self.x, self.y))
        for attack in self.attacks:
            attack.draw(window)
        self.healthbar(window)

    def cooldown(self):
        # attack is ready if cd_counter reaches the object's atk_cd
        if self.cd_counter >= self.atk_cd:
            self.cd_counter = 0
        elif self.cd_counter > 0:
            self.cd_counter += 1

    def attack(self, dx, dy, spd):
        if self.cd_counter == 0:
            # adjust which way the character will face
            if dx > 0:
                self.char_img = HIKARI
            elif dx < 0:
                self.char_img = pygame.transform.flip(HIKARI, True, False)
            # adjust the x/y coordinates a bit based on the image size (-7.5)
            new_attack = Attack(self.true_x-7.5, self.true_y-7.5, dx, dy, self.atk, spd, self.atk_img)
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
                # check if the self's attack hit any enemy among all the enemies
                for obj in objs:
                    if attack.collision(obj):
                        obj.health -= attack.dmg
                        obj.knocked_back(self.true_x, self.true_y, 0.5*obj.get_width())
                        if obj.health <= 0:
                            objs.remove(obj)
                        if attack in self.attacks: self.attacks.remove(attack)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.x - self.mov_spd > 0:   # left
            self.x -= self.mov_spd
            self.true_x -= self.mov_spd
        if keys[pygame.K_d] and self.x + self.mov_spd + self.get_width() < WIDTH:  # right
            self.x += self.mov_spd
            self.true_x += self.mov_spd
        if keys[pygame.K_w] and self.y - self.mov_spd > 0:     # up
            self.y -= self.mov_spd
            self.true_y -= self.mov_spd
        if keys[pygame.K_s] and self.y + self.mov_spd + self.get_height() < HEIGHT:  # down
            self.y += self.mov_spd
            self.true_y += self.mov_spd
        if keys[pygame.K_UP]:
            self.attack(0,-1, 15)
        if keys[pygame.K_DOWN]:
            self.attack(0, 1, 15)
        if keys[pygame.K_RIGHT]:
            self.attack(1, 0, 15)
        if keys[pygame.K_LEFT]:
            self.attack(-1, 0, 15)
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            dx, dy = x - self.true_x, y - self.true_y
            dist = math.sqrt(dx * dx + dy * dy)
            dx, dy = dx / dist, dy / dist
            self.attack(dx, dy, 15)

