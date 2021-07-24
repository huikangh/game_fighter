import pygame
import os

pygame.init()

# setting for game window
WIDTH, HEIGHT = 1200, 750
DISPLAY_BAR_HEIGHT = HEIGHT//20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Project Fighter")

# multiplier for displaying the image
SCALER = 0.035*WIDTH
SIZE_NORMAL = (35, 35)
SIZE_BOSS = (70, 70)

# load images of characters
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
RED_SPACE_SHIP = pygame.transform.scale(RED_SPACE_SHIP, SIZE_NORMAL)
GREEN_SPACE_SHIP = pygame.transform.scale(GREEN_SPACE_SHIP, SIZE_BOSS)
BLUE_SPACE_SHIP = pygame.transform.scale(BLUE_SPACE_SHIP, SIZE_NORMAL)
YELLOW_SPACE_SHIP = pygame.transform.scale(YELLOW_SPACE_SHIP, SIZE_NORMAL)

# Re-skin characters
HIKARI = pygame.image.load(os.path.join("assets", "Bullseye_Hikari2.png"))
GOBLIN = pygame.image.load(os.path.join("assets", "Goblin2.png"))
CROW = pygame.image.load(os.path.join("assets", "Crow2.png"))
GENTLEMAN_CROW = pygame.image.load(os.path.join("assets", "Gentleman_Crow2.png"))
TRUE_DEVIL_CAIN = pygame.image.load(os.path.join("assets", "True_Devil_Cain2.png"))
HIKARI = pygame.transform.scale(HIKARI, (50, 50))
GOBLIN = pygame.transform.scale(GOBLIN, (45, 45))
CROW = pygame.transform.scale(CROW, (40, 40))
GENTLEMAN_CROW = pygame.transform.scale(GENTLEMAN_CROW, (45, 45))
TRUE_DEVIL_CAIN = pygame.transform.scale(TRUE_DEVIL_CAIN, (70, 70))

# load images of lasers/bullets
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
RED_LASER = pygame.transform.scale(RED_LASER, SIZE_NORMAL)
GREEN_LASER = pygame.transform.scale(GREEN_LASER, SIZE_NORMAL)
BLUE_LASER  = pygame.transform.scale(BLUE_LASER, SIZE_NORMAL)
YELLOW_LASER  = pygame.transform.scale(YELLOW_LASER, SIZE_NORMAL)

# Re-skin attacks
WIND_ARROW = pygame.image.load(os.path.join("assets", "Wing_Arrow_Large2.png"))
PD_21_BULLET = pygame.image.load(os.path.join("assets", "PD-21_Bullet2.png"))
MD_21_BULLET = pygame.image.load(os.path.join("assets", "MD-21_Bullet2.png"))
WIND_ARROW = pygame.transform.scale(WIND_ARROW, (15, 35))
PD_21_BULLET = pygame.transform.scale(PD_21_BULLET, (15, 35))
MD_21_BULLET = pygame.transform.scale(MD_21_BULLET, (15, 35))

# load background image
BG = pygame.image.load(os.path.join("assets", "1140964.png"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT-DISPLAY_BAR_HEIGHT))

# sound files
pygame.mixer.init()
arrow_sound = pygame.mixer.Sound(os.path.join("assets", "Fire_Arrow2.mp3"))
laser_sound = pygame.mixer.Sound(os.path.join("assets", "Laser_Blast2.mp3"))
blast_sound = pygame.mixer.Sound(os.path.join("assets", "Blast2.mp3"))
pygame.mixer.music.load(os.path.join("assets", "Done_With_Work_David_Renda.mp3"))