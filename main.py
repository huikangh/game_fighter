import time
import random
import pygame
from assets import *
from character import *



# in-game parameters
fps = 60
level = 1
score = 0
pygame.font.init()
main_font = pygame.font.SysFont("comicsans", 35)

# main character
player = Hero(WIDTH//2, HEIGHT//2)



def redraw_window():
    WIN.fill((0,0,0))   # fill the surface with color black

    level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
    health_label = main_font.render(f"Score: {score}", 1, (255,255,255))
    WIN.blit(BG, (0, level_label.get_height()))                         # blit background image
    WIN.blit(level_label, (10, 0))                                      # blit text for level
    WIN.blit(health_label, (WIDTH-health_label.get_width()-10, 0))      # blit text for health

    player.draw(WIN)      # draw the character

    pygame.display.update()



def main():

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(fps)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # check for main character movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player.mov_spd > 0:   # left
            player.x -= player.mov_spd
        if keys[pygame.K_RIGHT] and player.x + player.mov_spd + player.get_width() < WIDTH:  # right
            player.x += player.mov_spd
        if keys[pygame.K_UP] and player.y - player.mov_spd > 0:     # up
            player.y -= player.mov_spd
        if keys[pygame.K_DOWN] and player.y + player.mov_spd + player.get_height() < HEIGHT:  # down
            player.y += player.mov_spd



main()