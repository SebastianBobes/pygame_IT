import pygame
import os
import subprocess
import sys
#from save_utils import  get_player_name, load_score

# Initializare Pygame
pygame.init()

# Ajustam display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Euroavia Game - Main Menu")

# Culori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 40)

# Score File
#SCORE_FILE = "score.txt"
#load_score()
#def load_score():
#    """ Load score from file or return 0 if not available. """
 #   if os.path.exists(SCORE_FILE):
  #      try:
   #         with open(SCORE_FILE, "r") as file:
    #            return int(file.read().strip())
     #   except ValueError:
      #      return 0
   # return 0

# Buton class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        """ Deseneaza buton """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        """ Verifica daca s-a apasat butonul """
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()

# Actiuni pentru butoane
def start_game():
    """ Da run la main.py """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # where PyInstaller extracts bundled files
    else:
        base_path = os.path.abspath(".")

    main_path = os.path.join(base_path, "main.py")
    with open(main_path, 'r') as f:
        exec(compile(f.read(), main_path, 'exec'), {'__name__': '__main__'})

def quit_game():
    """ Quit """
    pygame.quit()
    quit()

# Creare butoane
start_button = Button("Start", 200, 150, 200, 50, GREEN, (0, 255, 0), start_game)
quit_button = Button("Quit", 200, 230, 200, 50, RED, (255, 0, 0), quit_game)

# Bucla principala
running = True
while running:
    screen.fill(BLACK)

    # Afisare titlu
    title_text = font.render("Euroavia Main Menu", True, WHITE)
    screen.blit(title_text, (150, 50))

    # Afisare scor
   # score = load_score()
   # score_text = font.render(f"Total Score: {score}", True, BLUE)
   # screen.blit(score_text, (220, 100))

    # Deseneaza butoanele
    start_button.draw(screen)
    quit_button.draw(screen)

    # Verifica evenimente
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        start_button.check_click(event)
        quit_button.check_click(event)

    pygame.display.flip()

pygame.quit()
