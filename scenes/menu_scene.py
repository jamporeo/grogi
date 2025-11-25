# scenes/menu_scene.py
import pygame
from settings import *

class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 64)
        self.small_font = pygame.font.SysFont(None, 36)
        self.running = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.running = False  # Sale del menú

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        title = self.font.render("Pastel de Papa Salvamundos", True, WHITE)
        hint = self.small_font.render("Presiona ENTER para comenzar", True, LIGHT_YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 400))
        pygame.display.flip()