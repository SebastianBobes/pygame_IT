import pygame
import os
import subprocess
import sys

# Initializare
pygame.quit()  
pygame.init()


PLAYER_FILE = "player.txt"


if os.path.exists(PLAYER_FILE):
    pygame.quit()
    subprocess.Popen([sys.executable, "menu.py"]) 
    sys.exit()

# Display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Setup - Enter Your Name")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)

# Player name
player_name = ""

# Bucla principala
running = True
while running:
    screen.fill(BLACK)

    title_text = font.render("Enter Your Name:", True, WHITE)
    screen.blit(title_text, (200, 100))

    # Display input text
    name_text = font.render(player_name + "|", True, BLUE)
    screen.blit(name_text, (200, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and player_name.strip():
                # Save player name
                with open(PLAYER_FILE, "w") as file:
                    file.write(player_name.strip())

                print(f"Player name '{player_name.strip()}' saved. Launching menu...")

                pygame.display.quit()
                pygame.quit()
                
                subprocess.Popen([sys.executable, "menu.py"])
                sys.exit()

            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                if len(player_name) < 20 and event.unicode.isalnum():
                    player_name += event.unicode

    pygame.display.flip()

pygame.quit()
sys.exit()
