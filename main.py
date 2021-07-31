from button import *
from character import *



# in-game parameters
fps = 60
level = 0
enemy_count = 0
pygame.font.init()
counter_font = pygame.font.SysFont("comicsans", 35)
message_font = pygame.font.SysFont("comicsans", 50)
game_over = 0
over_counter = 0

# main character
player = Hero(WIDTH/2-(35/2), HEIGHT/2-(35/2))
# enemies
enemies = []
enemies_attacks = []
endless_waves = [[0, 0, 0]]
adventure_waves = [[5, 0, 0],
                   [0, 5, 0],
                   [4, 4, 0],
                   [7, 7, 0],
                   [0, 0, 1]]



def redraw_window(game_mode):
    WIN.fill((0,0,0))   # fill the surface with color black

    # redraw game mode and level/enemy counter
    mode = "Adventure Mode" if game_mode == 1 else "Endless Mode"
    mode_label = counter_font.render(mode, 1, (255,255,255))
    level_label = counter_font.render(f"Level: {level}", 1, (255,255,255))
    enemy_label = counter_font.render(f"Enemies: {enemy_count}", 1, (255,255,255))
    WIN.blit(BG, (0, DISPLAY_BAR_HEIGHT))                         # blit background image
    WIN.blit(mode_label, (20, (DISPLAY_BAR_HEIGHT - level_label.get_height()) / 2))
    WIN.blit(enemy_label, (WIDTH-enemy_label.get_width()-20,
                           (DISPLAY_BAR_HEIGHT-enemy_label.get_height())/2))
    WIN.blit(level_label, (WIDTH-enemy_label.get_width()-60-level_label.get_width(),
                           (DISPLAY_BAR_HEIGHT-level_label.get_height())/2))

    # redraw enemies and player
    for enemy in enemies:
        enemy.draw(WIN)
    for attack in enemies_attacks:
        attack.draw(WIN)
    player.draw(WIN)

    # check for game state
    if game_over == -1:
        lost_label = message_font.render(f"You've lost!", 1, (255,255,255))
        WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))
    elif game_over == 1:
        won_label = message_font.render(f"You've won!", 1, (255,255,255))
        WIN.blit(won_label, (WIDTH/2 - won_label.get_width()/2, HEIGHT/2 - won_label.get_height()/2))



def game_pause(pause, window, events):
    button = None
    if not pause:
        button = Button(WIDTH / 2 - 100 / 2, 0, 100, DISPLAY_BAR_HEIGHT, (0, 0, 0), (255, 255, 255), "Pause")
    else:
        button = Button(WIDTH / 2 - 100 / 2, 0, 100, DISPLAY_BAR_HEIGHT, (0, 0, 0), (255, 255, 255), "Resume")
    button.draw(window)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.clicked(event.pos):
                pause = not pause
        if event.type == pygame.QUIT:
            quit()
    return pause



def reset():
    global level, enemy_count, game_over, over_counter, player, enemies, enemies_attacks, endless_waves
    level = 0
    enemy_count = 0
    game_over = 0
    over_counter = 0
    player = Hero(WIDTH // 2, HEIGHT // 2)
    enemies = []
    enemies_attacks = []
    endless_waves = [[0,0,0]]



# game_mode: 1->Adventure, 2->Endless
def main(game_mode):
    global fps, level, enemy_count, endless_waves, adventure_waves, game_over, over_counter

    run = True
    pause = False
    clock = pygame.time.Clock()

    while run:
        clock.tick(fps)
        events = pygame.event.get()                 # retrieve all the pygame events
        redraw_window(game_mode)                    # redraw the UI
        pause = game_pause(pause, WIN, events)      # check for game pause/unpause
        pygame.display.update()                     # update/display what we drew
        if pause:
            continue

        # check for game over (lost)
        if player.health <= 0:
            game_over = -1
        if game_over:
            over_counter += 1
            if over_counter > fps*3:
                run = False
            else:
                continue

        # check game mode:
        waves = None
        if game_mode == 1:
            waves = adventure_waves
            player.atk_cd = 45
        elif game_mode == 2:
            waves = endless_waves
            player.atk_cd = 15

        # spawn enemies if a level is cleared
        enemy_count = len(enemies)
        if len(enemies) == 0:
            level += 1
            # check for game over (won) if in adventure mode
            if game_mode == 1 and level > len(waves):
                game_over = 1
                continue
            # increment number of enemies if in endless mode
            if game_mode == 2:
                new_wave = waves[-1]
                if new_wave[0] > new_wave[1]:
                    new_wave[1] += 2
                else:
                    new_wave[0] += 2
                waves[-1] = new_wave
            # spawn enemies
            wave_size = waves[level-1] if game_mode == 1 else waves[-1]
            red = wave_size[0]
            blue = wave_size[1]
            boss = wave_size[2]
            for i in range(sum(wave_size)):
                # randomly choose where the enemy would spawn
                randx, randy = 0, 0
                side = random.choice(["left","right","top","bottom"])
                if side == "left":
                    randx, randy = random.randrange(-1000, -100), random.randrange(0, HEIGHT)
                elif side == "right":
                    randx, randy = random.randrange(WIDTH+100, WIDTH+1000), random.randrange(0, HEIGHT)
                elif side == "top":
                    randx, randy = random.randrange(0, WIDTH), random.randrange(-1000,-100)
                elif side == "bottom":
                    randx, randy = random.randrange(0, WIDTH), random.randrange(HEIGHT+100, HEIGHT+1000)
                if i < red:
                    enemy = Enemy(randx, randy)
                elif i < red+blue:
                    enemy = EnemyRanged(randx, randy)
                else:
                    enemy = EnemyBoss(randx, randy)
                enemies.append(enemy)

        # check if the player quits the game
        for event in events:
            if event.type == pygame.QUIT:
                quit()

        # check for player movement/attack
        player.move()

        # move the player's attack, and check for any attack collision
        player.move_attack(enemies)

        # update each enemy's movement and action
        for enemy in enemies[:]:
            # Enemy:MELEE
            enemy.chase(player.true_x, player.true_y)
            dx, dy = enemy.calc_dxdy(player.true_x, player.true_y)
            # Enemy:RANGED
            if type(enemy) is EnemyRanged:
                enemy.cooldown()
                new_attack = enemy.attack(dx, dy, 5)
                if new_attack:
                    enemies_attacks.append(new_attack)
            # Enemy:BOSS
            elif type(enemy) is EnemyBoss:
                # chase if off-screen, else hoover in screen
                enemy.cooldown()
                boss_attack = enemy.attack(dx, dy, 5)
                if boss_attack:
                    for shot in boss_attack:
                        enemies_attacks.append(shot)
            if collide(enemy, player):
                player.health -= enemy.atk
                player.knocked_back(enemy.true_x, enemy.true_y, player.get_width())

        # move the enemies' attack
        for attack in enemies_attacks[:]:
            attack.move()
            if attack.off_screen(WIDTH, HEIGHT):
                enemies_attacks.remove(attack)
            else:
                if attack.collision(player):
                    player.health -= attack.dmg
                    player.knocked_back(attack.true_x, attack.true_y, 0.5*player.get_width())
                    if attack in enemies_attacks: enemies_attacks.remove(attack)


def main_menu():
    # background music
    #pygame.mixer.music.play(-1)

    # buttons on the menu
    button1 = Button(WIDTH/2-200/2, HEIGHT/2-50/2,       210, 40, (55,110,219), (0,0,0), "Adventure Mode")
    button2 = Button(WIDTH/2-200/2, (HEIGHT/2-50/2)+60,  210, 40, (55,110,219), (0,0,0), "Endless Mode")
    button3 = Button(WIDTH/2-200/2, (HEIGHT/2-50/2)+120, 210, 40, (55,110,219), (0,0,0), "Exit Game")

    run = True
    while run:
        reset()
        # main_menu background
        WIN.fill((0, 0, 0))
        WIN.blit(BG, (0,DISPLAY_BAR_HEIGHT))
        # title
        title_font = pygame.font.SysFont("comicsans", 100)
        title_label = title_font.render("PROJECT: FIGHTER", 1, (55,110,219))
        WIN.blit(title_label, (WIDTH/2-title_label.get_width()/2, HEIGHT/4))
        # redraw_buttons
        button1.draw(WIN)
        button2.draw(WIN)
        button3.draw(WIN)
        # refresh
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.clicked(event.pos):
                    main(1)
                elif button2.clicked(event.pos):
                    main(2)
                elif button3.clicked(event.pos):
                    run = False

    quit()



main_menu()