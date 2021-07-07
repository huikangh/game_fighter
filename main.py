import time
import random
import character
from assets import *


# in-game parameters
fps = 60
level = 1
score = 0
pygame.font.init()
main_font = pygame.font.SysFont("comicsans", 35)


def redraw_window():
    WIN.fill((0,0,0))   # fill the surface with color black
    level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
    health_label = main_font.render(f"Score: {score}", 1, (255,255,255))
    WIN.blit(BG, (0, level_label.get_height()))                         # background image
    WIN.blit(level_label, (10, 0))                                      # text for level
    WIN.blit(health_label, (WIDTH-health_label.get_width()-10, 0))      # text for health

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


main()