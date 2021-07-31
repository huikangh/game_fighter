import pygame
import os

pygame.init()

# setting for game window
WIDTH, HEIGHT = 1200, 750
DISPLAY_BAR_HEIGHT = HEIGHT//20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Project: Fighter")

# load images of characters
HIKARI = pygame.image.load(os.path.join("assets", "Bullseye_Hikari2.png")).convert_alpha()
GOBLIN = pygame.image.load(os.path.join("assets", "Goblin2.png")).convert_alpha()
CROW = pygame.image.load(os.path.join("assets", "Crow2.png")).convert_alpha()
TRUE_DEVIL_CAIN = pygame.image.load(os.path.join("assets", "True_Devil_Cain2.png")).convert_alpha()
HIKARI = pygame.transform.scale(HIKARI, (50, 50))
GOBLIN = pygame.transform.scale(GOBLIN, (45, 45))
CROW = pygame.transform.scale(CROW, (40, 40))
TRUE_DEVIL_CAIN = pygame.transform.scale(TRUE_DEVIL_CAIN, (70, 70))

# load images of attacks
WIND_ARROW = pygame.image.load(os.path.join("assets", "Wing_Arrow_Large2.png")).convert_alpha()
PD_21_BULLET = pygame.image.load(os.path.join("assets", "PD-21_Bullet3.png")).convert_alpha()
MD_21_BULLET = pygame.image.load(os.path.join("assets", "MD-21_Bullet2.png")).convert_alpha()
WIND_ARROW = pygame.transform.scale(WIND_ARROW, (15, 35))
PD_21_BULLET = pygame.transform.scale(PD_21_BULLET, (15, 35))
MD_21_BULLET = pygame.transform.scale(MD_21_BULLET, (15, 35))

# load background image
BG = pygame.image.load(os.path.join("assets", "sand3.png")).convert_alpha()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT-DISPLAY_BAR_HEIGHT))

# sound files
pygame.mixer.init()
arrow_sound = pygame.mixer.Sound(os.path.join("assets", "Fire_Arrow2.mp3"))
fire_sound = pygame.mixer.Sound(os.path.join("assets", "Fire_Woosh2.mp3"))
blast_sound = pygame.mixer.Sound(os.path.join("assets", "Blast2.mp3"))
pygame.mixer.music.load(os.path.join("assets", "purrple-cat-field-of-fireflies.mp3"))

# Field Of Fireflies by Purrple Cat | https://purrplecat.com/
# Music promoted on https://www.chosic.com/
# Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
# https://creativecommons.org/licenses/by-sa/3.0/
