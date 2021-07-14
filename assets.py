import pygame
import os

# setting for game window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Project Fighter")

# size for displaying the image
SIZE_NORMAL = (35, 35)


# load images of characters
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
RED_SPACE_SHIP = pygame.transform.scale(RED_SPACE_SHIP, SIZE_NORMAL)
GREEN_SPACE_SHIP = pygame.transform.scale(GREEN_SPACE_SHIP, SIZE_NORMAL)
YELLOW_SPACE_SHIP = pygame.transform.scale(YELLOW_SPACE_SHIP, SIZE_NORMAL)

# load images of lasers/bullets
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
GREEN_LASER  = pygame.transform.scale(GREEN_LASER, SIZE_NORMAL)
YELLOW_LASER  = pygame.transform.scale(YELLOW_LASER, SIZE_NORMAL)


# load background image
BG = pygame.image.load(os.path.join("assets", "background-black.png"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
