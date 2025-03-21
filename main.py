import pygame
import random
import os

# Initializare
pygame.init()

# Ajustam display
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("euroavia")

# Culori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Font numar pasi
font = pygame.font.Font(None, 36)

# Funcție pentru salvare/scor
SCORE_FILE = "score.txt"

def load_score():
    """ Luam scor din fisier sau il initializam cu 0 """
    # Ne asiguram ca exista fisierul
    open(SCORE_FILE, "a").close()

    try:
        with open(SCORE_FILE, "r") as file:
            data = file.read().strip()
            return int(data) if data else 0 
    except ValueError:
        print("Eroare citire fisier.")
        return 0

def save_score(score):
    """ Salvam noua valoare a scorului """
    total_score = load_score() + score
    with open(SCORE_FILE, "w") as file:
        file.write(str(total_score))
    print(f"Score salvat: {total_score}")  #  Pentru debug

# Atribute pentru caracter
player_x, player_y = 0, 0 
steps = 0

# Atribute bot
bot_x, bot_y = 9, 9

# Obstacol
obstacles = set()
while len(obstacles) < 15:  # Numar obstacole
    ox, oy = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
    if (ox, oy) not in {(player_x, player_y), (bot_x, bot_y)}:  # Evita spawn-ul pe player/bot
        obstacles.add((ox, oy))

# Miscare bot catre jucator
def bot_move(bot_x, bot_y, player_x, player_y, obstacles):
    options = []
    if player_x > bot_x and (bot_x + 1, bot_y) not in obstacles:  
        options.append((bot_x + 1, bot_y))
    if player_x < bot_x and (bot_x - 1, bot_y) not in obstacles:  
        options.append((bot_x - 1, bot_y))
    if player_y > bot_y and (bot_x, bot_y + 1) not in obstacles:  
        options.append((bot_x, bot_y + 1))
    if player_y < bot_y and (bot_x, bot_y - 1) not in obstacles:  
        options.append((bot_x, bot_y - 1))
    
    if options:
        bot_x, bot_y = random.choice(options)  # Alege random o pozitie
    
    return bot_x, bot_y

# Bucla principala
running = True
walking = True
game_over = False  

while running:
    screen.fill(BLACK)  
    
    # Desenam grid-ul si obstacolele
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (col, row) in obstacles:
                pygame.draw.rect(screen, BLUE, rect)  # Desenam obstacole
            pygame.draw.rect(screen, GRAY, rect, 1)  # Desenam conturul fiecarei casute
    
    player_image = pygame.image.load("Capture.jpg") 
    player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))
    # Afisare jucator
    screen.blit(player_image, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    bot_image = pygame.image.load("police.jpg")
    bot_image = pygame.transform.scale(bot_image, (CELL_SIZE, CELL_SIZE))
    # Afisare bot
    screen.blit(bot_image, (bot_x * CELL_SIZE, bot_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Afisare numar pasi
    counter_text = font.render(f"Steps: {steps}", True, WHITE)
    screen.blit(counter_text, (10, 10))

    # Afisare scor total din fisier
    total_score = load_score()
    total_score_text = font.render(f"Total Score: {total_score}", True, WHITE)
    screen.blit(total_score_text, (10, 40))

    # Evenimente
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    if walking and not game_over:
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y
        
        if keys[pygame.K_a] and player_x > 0 and (player_x - 1, player_y) not in obstacles:  
            new_x -= 1
        if keys[pygame.K_d] and player_x < COLS - 1 and (player_x + 1, player_y) not in obstacles:  
            new_x += 1
        if keys[pygame.K_w] and player_y > 0 and (player_x, player_y - 1) not in obstacles:  
            new_y -= 1
        if keys[pygame.K_s] and player_y < ROWS - 1 and (player_x, player_y + 1) not in obstacles:  
            new_y += 1

        if (new_x, new_y) != (player_x, player_y):  # Daca s-a facut o miscare valida
            player_x, player_y = new_x, new_y
            steps += 1
            bot_x, bot_y = bot_move(bot_x, bot_y, player_x, player_y, obstacles)  

        if (bot_x, bot_y) == (player_x, player_y):
            game_over = True  
            walking = False 
            save_score(steps)  # Salvează scorul înainte de a termina jocul
            

    # Afisare Game Over
    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
    
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
