import pygame
import random
import os
import psycopg2

harti = ["harta1.txt", "harta2.txt", "harta3.txt", "harta4.txt", "harta5.txt"]
k = 0

def get_player_name():
    try:
        with open("player.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Error: name.txt not found. Using default name.")
        return "UnknownPlayer"

def get_player_score():
    try:
        with open("score.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Error: score.txt not found. Using default score.")
        return 0

DATABASE_URL = "adresa_baza_date"

def connect_db():
    try:
        return psycopg2.connect(DATABASE_URL, sslmode="require")
    except Exception as e:
        print("Database Connection Error:", e)
        return None

def save_score_db(player_name, score):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO joc (nume, scor) VALUES (%s, %s)", (player_name, score))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Score saved: {player_name} - {score}")
        except Exception as e:
            print("Error saving score:", e)

# Inițializare pygame
pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("euroavia")

# Culori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)
SCORE_FILE = "score.txt"

# Texturi player și bot
player_texture = pygame.image.load("player.jpg")
player_texture = pygame.transform.scale(player_texture, (CELL_SIZE, CELL_SIZE))

bot_texture = pygame.image.load("bot.jpg")
bot_texture = pygame.transform.scale(bot_texture, (CELL_SIZE, CELL_SIZE))

def load_score():
    open(SCORE_FILE, "a").close()
    try:
        with open(SCORE_FILE, "r") as file:
            data = file.read().strip()
            return int(data) if data else 0
    except ValueError:
        print("Eroare citire fisier.")
        return 0

def save_score(score):
    total_score = load_score() + score
    with open(SCORE_FILE, "w") as file:
        file.write(str(total_score))
    print(f"Score salvat: {total_score}")

player_name = get_player_name()
score = get_player_score()

player_x, player_y = 0, 0
steps = 0
bot_x, bot_y = 9, 9

def creare_harti(k):
    i, j = 0, 0
    global obstacles
    obstacles = set()
    harta = harti[k]

    with open(harta, 'r') as file:
        for line in file:
            numbers = line.strip().split()
            for num in numbers:
                if j >= 10:
                    i += 1
                    j = 0
                if num == '0':
                    obstacles.add((i, j))
                j += 1
    return obstacles

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
        bot_x, bot_y = random.choice(options)
    return bot_x, bot_y

# Încarcă prima hartă
obstacles = creare_harti(k)

running = True
walking = True
game_over = False
won = False
over = False

while running:
    screen.fill(BLACK)

    # Desenează grid și obstacole
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (col, row) in obstacles:
                pygame.draw.rect(screen, BLUE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Texturi player și bot
    screen.blit(player_texture, (player_x * CELL_SIZE, player_y * CELL_SIZE))
    screen.blit(bot_texture, (bot_x * CELL_SIZE, bot_y * CELL_SIZE))

    # Afișare scor
    counter_text = font.render(f"Steps: {steps}", True, WHITE)
    screen.blit(counter_text, (10, 10))

    total_score = load_score()
    total_score_text = font.render(f"Total Score: {total_score}", True, WHITE)
    screen.blit(total_score_text, (10, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    if walking and not game_over and not won:
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

        if (new_x, new_y) != (player_x, player_y):
            player_x, player_y = new_x, new_y
            steps += 1
            bot_x, bot_y = bot_move(bot_x, bot_y, player_x, player_y, obstacles)

        if (bot_x, bot_y) == (player_x, player_y):
            game_over = True
            walking = False
            save_score(steps)
        if (player_x, player_y) == (9, 9):
            won = True
            save_score(steps)

    if game_over and not over:
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
        save_score_db(player_name, score)
        over = True

    if won and not over:
        if k < len(harti) - 1:
            k += 1
            player_x, player_y = 0, 0
            bot_x, bot_y = 9, 9
            steps = 0
            obstacles.clear()
            obstacles = creare_harti(k)
            walking = True
            game_over = False
            won = False
            over = False
        else:
            won_text = font.render("You won the game!", True, WHITE)
            screen.blit(won_text, (WIDTH // 2 - 150, HEIGHT // 2))
            over = True

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
