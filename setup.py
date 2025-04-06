import pygame
import os
import subprocess
import sys

# Hidden path (Windows only)
APPDATA = os.getenv('APPDATA')
HIDDEN_DIR = os.path.join(APPDATA, 'game_data')
os.makedirs(HIDDEN_DIR, exist_ok=True)

PLAYER_FILE = os.path.join(HIDDEN_DIR, "player.txt")

# Check if player.txt already exists
if os.path.exists(PLAYER_FILE):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # PyInstaller temp folder
    else:
        base_path = os.path.abspath(".")

    menu_path = os.path.join(base_path, "menu.py")
    with open(menu_path, 'r') as f:
        exec(compile(f.read(), menu_path, 'exec'), {'__name__': '__main__'})
    sys.exit()

# Init pygame
pygame.init()

# Display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Setup - Enter Your Name")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)

# Player name input
player_name = ""

# Game loop
running = True
while running:
    screen.fill(BLACK)

    title_text = font.render("Enter Your Name:", True, WHITE)
    screen.blit(title_text, (200, 100))

    name_text = font.render(player_name + "|", True, BLUE)
    screen.blit(name_text, (200, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and player_name.strip():
                # Save the name
                with open(PLAYER_FILE, "w") as file:
                    file.write(player_name.strip())

                print(f"Player name '{player_name.strip()}' saved. Launching menu...")

                pygame.quit()

                if getattr(sys, 'frozen', False):
                    base_path = sys._MEIPASS
                else:
                    base_path = os.path.abspath(".")

                menu_path = os.path.join(base_path, "menu.py")
                subprocess.Popen([sys.executable, menu_path])
                sys.exit()

            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                if len(player_name) < 20 and event.unicode.isalnum():
                    player_name += event.unicode

    pygame.display.flip()

pygame.quit()
sys.exit()
