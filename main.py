import time
import random
import pygame
from assets import *
from character import *



# in-game parameters
fps = 60
level = 0
score = 0
pygame.font.init()
main_font = pygame.font.SysFont("comicsans", 35)

# main character
player = Hero(WIDTH//2, HEIGHT//2)
# enemies
enemies = []
waves = [5, 10, 15]



def redraw_window():
    WIN.fill((0,0,0))   # fill the surface with color black

    level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
    health_label = main_font.render(f"Score: {score}", 1, (255,255,255))
    WIN.blit(BG, (0, level_label.get_height()))                         # blit background image
    WIN.blit(level_label, (10, 0))                                      # blit text for level
    WIN.blit(health_label, (WIDTH-health_label.get_width()-10, 0))      # blit text for health

    for enemy in enemies:   # draw the enemies
        enemy.draw(WIN)
    player.draw(WIN)        # draw the main character

    pygame.display.update()



def main():
    global fps, level, score, waves

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(fps)
        redraw_window()

        # check for game over
        if player.health <= 0:
            lost = True
        # spawn wave of enemies
        if len(enemies) == 0:
            level += 1
            if level > len(waves):
                print("You've won!")
                break
            wave_size = waves[level-1]
            for i in range(wave_size):
                randx, randy = 0, 0
                side = random.choice(["left","right","top","bottom"])  # randomly choose where the enemy would spawn
                if side == "left":
                    randx, randy = random.randrange(-500, -100), random.randrange(0, HEIGHT)
                elif side == "right":
                    randx, randy = random.randrange(WIDTH+100, WIDTH+500), random.randrange(0, HEIGHT)
                elif side == "top":
                    randx, randy = random.randrange(0, WIDTH), random.randrange(-500,-100)
                elif side == "bottom":
                    randx, randy = random.randrange(0, WIDTH), random.randrange(HEIGHT+100, HEIGHT+500)
                enemy = EnemyRed(randx, randy)
                enemies.append(enemy)

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
        if keys[pygame.K_w]:
            player.attack("w")
        if keys[pygame.K_a]:
            player.attack("a")
        if keys[pygame.K_s]:
            player.attack("s")
        if keys[pygame.K_d]:
            player.attack("d")

        # make each enemy move towards the player
        for enemy in enemies[:]:
            enemy.chase(player.x, player.y)

        # move the player's attack, and check for any attack collision
        score += player.move_attack(enemies)        # move_attack return number of enemies killed

    pygame.quit()


# main function
main()