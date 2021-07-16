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
counter_font = pygame.font.SysFont("comicsans", 35)
message_font = pygame.font.SysFont("comicsans", 50)
gameover = 0
over_counter = 0

# main character
player = Hero(WIDTH//2, HEIGHT//2)
# enemies
enemies = []
enemies_attacks = []
waves = [[5, 0, 0],
         [0, 5, 0],
         [5, 5, 0],
         [5,10, 0],
         [0, 0, 1]]



def redraw_window():
    WIN.fill((0,0,0))   # fill the surface with color black

    level_label = counter_font.render(f"Level: {level}", 1, (255,255,255))
    score_label = counter_font.render(f"Score: {score}", 1, (255,255,255))
    WIN.blit(BG, (0, level_label.get_height()))                         # blit background image
    WIN.blit(level_label, (10, 0))                                      # blit text for level
    WIN.blit(score_label, (WIDTH-score_label.get_width()-10, 0))      # blit text for health

    for enemy in enemies:   # draw the enemies
        enemy.draw(WIN)
    for attack in enemies_attacks:
        attack.draw(WIN)
    player.draw(WIN)        # draw the main character

    if gameover == -1:
        lost_label = message_font.render(f"You've lost!", 1, (255,255,255))
        WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))
    elif gameover == 1:
        won_label = message_font.render(f"You've won!", 1, (255,255,255))
        WIN.blit(won_label, (WIDTH/2 - won_label.get_width()/2, HEIGHT/2 - won_label.get_height()/2))

    pygame.display.update()



def main():
    global fps, level, score, waves, gameover, over_counter

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(fps)
        redraw_window()

        # check for game over (lost)
        if player.health <= 0:
            gameover = -1
        if gameover:
            over_counter += 1
            if over_counter > fps*3:
                break
            else:
                continue

        # spawn wave of enemies
        if len(enemies) == 0:
            level += 1
            # check for game over (won)
            if level > len(waves):
                gameover = 1
                continue
            wave_size = waves[level-1]
            red = wave_size[0]
            blue = wave_size[1]
            boss = wave_size[2]
            for i in range(sum(wave_size)):
                randx, randy = 0, 0
                side = random.choice(["left","right","top","bottom"])  # randomly choose where the enemy would spawn
                if side == "left":
                    randx, randy = random.randrange(-1000, -100), random.randrange(0, HEIGHT)
                elif side == "right":
                    randx, randy = random.randrange(WIDTH+100, WIDTH+1000), random.randrange(0, HEIGHT)
                elif side == "top":
                    randx, randy = random.randrange(0, WIDTH), random.randrange(-1000,-100)
                elif side == "bottom":
                    randx, randy = random.randrange(0, WIDTH), random.randrange(HEIGHT+100, HEIGHT+1000)
                if i < red:
                    enemy = EnemyRed(randx, randy)
                elif i < red+blue:
                    enemy = EnemyBlue(randx, randy)
                else:
                    enemy = EnemyBoss(randx, randy)
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

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
            player.attack(0,-1, 15)
        if keys[pygame.K_a]:
            player.attack(-1, 0, 15)
        if keys[pygame.K_s]:
            player.attack(0, 1, 15)
        if keys[pygame.K_d]:
            player.attack(1, 0, 15)

        # update each enemy's movement and action
        for enemy in enemies[:]:
            # Enemy:MELEE
            if isinstance(enemy, EnemyRed):
                enemy.chase(player.x, player.y)
            # Enemy:RANGED
            elif isinstance(enemy, EnemyBlue):
                enemy.chase(player.x, player.y)
                enemy.cooldown()
                dx,dy = enemy.calc_dxdy(player.x, player.y)
                new_attack = enemy.attack(dx, dy, 5)
                if new_attack:
                    enemies_attacks.append(new_attack)
            # Enemy:BOSS
            elif isinstance(enemy, EnemyBoss):
                # chase if off-screen, else hoover in screen
                enemy.chase(player.x, player.y)
                enemy.cooldown()
                dx, dy = enemy.calc_dxdy(player.x, player.y)
                boss_attack = enemy.attack(dx, dy, 5)
                if boss_attack:
                    for shot in boss_attack:
                        enemies_attacks.append(shot)
            if collide(enemy, player):
                player.health -= enemy.atk
                player.knocked_back(enemy.x, enemy.y, player.get_width())

        # move the player's attack, and check for any attack collision
        score += player.move_attack(enemies)        # move_attack return number of enemies killed

        # move the enemies' attack
        for attack in enemies_attacks[:]:
            attack.move()
            if attack.off_screen(WIDTH, HEIGHT):
                enemies_attacks.remove(attack)
            else:
                if attack.collision(player):
                    player.health -= attack.dmg
                    player.knocked_back(attack.x, attack.y, 0.5*player.get_width())
                    if attack in enemies_attacks: enemies_attacks.remove(attack)



# main function
main()