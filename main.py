
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
new_x, new_y= 0, 0
steps = 0


#Obstacol
obstacles = set()
for _ in range(15):  # Numar obstacole
    ox, oy = random.randint(0, COLS-1), random.randint(0, ROWS-1)
    if (ox, oy) != (player_x, player_y):  # Masura de precautie pentru a nu fi blocat jucatorul de la inceput
        obstacles.add((ox, oy))

# Anuleaza input lag-ul
pygame.key.set_repeat(500, 500)

# Bucla principala
running = True
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
        screen, RED, 
        (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
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
    else: new_x, new_y = player_x, player_y

    # Actualizare display
    pygame.display.flip()

    # FPS
    pygame.time.delay(100)

# Quit
pygame.quit()
