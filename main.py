import pygame
import random

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
pygame.font.init()
font = pygame.font.Font(None, 36)

# Atribute pentru caracter
player_x, player_y = 0, 0 
new_x, new_y = 0, 0
steps = 0

# Atribute bot
bot_x, bot_y = 9, 9

# Obstacol
obstacles = set()
for _ in range(15):  # Numar obstacole
    ox, oy = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
    if (ox, oy) != (player_x, player_y):  # Masura de precautie pentru a nu fi blocat jucatorul de la inceput
        obstacles.add((ox, oy))

# Anuleaza input lag-ul
pygame.key.set_repeat(500, 500)

# Bot movement
def bot(bot_x, bot_y, player_x, player_y, obstacles):
    difx = player_x - bot_x
    dify = player_y - bot_y
    
    # Try to move the bot towards the player
    if difx == 0 and dify < 0:
        if (bot_x, bot_y - 1) not in obstacles:
            bot_x, bot_y = bot_x, bot_y - 1
    elif difx == 0 and dify > 0:
        if (bot_x, bot_y + 1) not in obstacles:
            bot_x, bot_y = bot_x, bot_y + 1
    elif difx > 0 and dify > 0:
        if (bot_x, bot_y + 1) not in obstacles:
            bot_x, bot_y = bot_x, bot_y + 1
        elif (bot_x + 1, bot_y) not in obstacles:
            bot_x, bot_y = bot_x + 1, bot_y
    elif difx > 0 and dify < 0:
        if (bot_x, bot_y - 1) not in obstacles:
            bot_x, bot_y = bot_x, bot_y - 1
        elif (bot_x + 1, bot_y) not in obstacles:
            bot_x, bot_y = bot_x + 1, bot_y
    elif difx < 0 and dify > 0:
        if (bot_x, bot_y + 1) not in obstacles:
            bot_x, bot_y = bot_x, bot_y + 1
        elif (bot_x - 1, bot_y) not in obstacles:
            bot_x, bot_y = bot_x - 1, bot_y
    elif difx < 0 and dify < 0:
        if (bot_x, bot_y - 1) not in obstacles:
            bot_x, bot_y = bot_x, bot_y - 1
        elif (bot_x - 1, bot_y) not in obstacles:
            bot_x, bot_y = bot_x - 1, bot_y
    elif difx > 0 and dify == 0:
        if (bot_x + 1, bot_y) not in obstacles:
            bot_x, bot_y = bot_x + 1, bot_y
    elif difx < 0 and dify == 0:
        if (bot_x - 1, bot_y) not in obstacles:
            bot_x, bot_y = bot_x - 1, bot_y

    return bot_x, bot_y
walking=True
# Bucla principala
running = True
player_moved = False  # Flag to track if the player has moved

while running:
    screen.fill(BLACK)  
    
    # Desenam grid-ul si obstacolele
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (col, row) in obstacles:
                pygame.draw.rect(screen, BLUE, rect)  # Desenam obstacole
                pygame.draw.rect(screen, GRAY, rect, 1)  # Desenam conturul fiecarei casute
    
    # Afisare jucator
    pygame.draw.rect(
        screen, WHITE, 
        (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )
    
    # Afisare bot
    pygame.draw.rect(
        screen, RED, 
        (bot_x * CELL_SIZE, bot_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )
    
    # Afisare numar pasi
    counter_text = font.render(f"Steps: {steps}", True, WHITE)
    screen.blit(counter_text, (10, 10))

    # Modul prin care iesim din program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Miscare
    keys = pygame.key.get_pressed()
    if walking == True: 
        if keys[pygame.K_a] and (player_x - 1, player_y) not in obstacles and player_x > 0:  # Stanga
            new_x -= 1
        if keys[pygame.K_d] and (player_x + 1, player_y) not in obstacles and player_x < COLS - 1:  # Dreapta
            new_x += 1
        if keys[pygame.K_w] and (player_x, player_y - 1) not in obstacles and player_y > 0:  # Sus
            new_y -= 1
        if keys[pygame.K_s] and (player_x, player_y + 1) not in obstacles and player_y < ROWS - 1:  # Jos
            new_y += 1

    # Verificare daca casuta selectata e obstacol
    if (new_x, new_y) not in obstacles and (new_x, new_y) != (player_x, player_y):
            player_x, player_y = new_x, new_y
            steps += 1
            player_moved = True  # Set player move flag
    else: 
        new_x, new_y = player_x, player_y

    # Only move the bot if the player has moved
    if player_moved:
        bot_x, bot_y = bot(bot_x, bot_y, player_x, player_y, obstacles)  # Update bot position
        player_moved = False  # Reset flag after bot moves
    
    #Game over
    if (bot_x, bot_y) == (player_x, player_y):
            counter_text = font.render(f"Game Over", True, WHITE)
            screen.blit(counter_text, (350, 350))
            walking= False
    # Actualizare display
    pygame.display.flip()

    # FPS
    pygame.time.delay(100)

# Quit
pygame.quit()
