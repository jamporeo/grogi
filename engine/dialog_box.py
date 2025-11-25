# engine/dialog_box.py
import pygame
from settings import *

class DialogBox:
    def __init__(self, font_size=24):
        self.font = pygame.font.Font(DEFAULT_FONT, font_size) if DEFAULT_FONT else pygame.font.SysFont(None, font_size)
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT // 4
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - self.height, self.width, self.height)
        self.text = ""
        self.visible = False

    def set_text(self, text):
        self.text = text
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return
        # Fondo del cuadro de diálogo
        pygame.draw.rect(screen, DARK_GRAY, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        # Renderizar texto con salto de línea
        lines = self._split_text(self.text, self.width - 40)
        y_offset = self.rect.top + 20
        for line in lines:
            text_surface = self.font.render(line, True, LIGHT_YELLOW)
            screen.blit(text_surface, (self.rect.left + 20, y_offset))
            y_offset += 30

    def _split_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines