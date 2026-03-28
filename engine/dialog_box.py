# engine/dialog_box.py
import pygame
import os

# Asumimos que este archivo está en una carpeta "engine", y el proyecto raíz tiene "assets/fonts/Font.ttf"
FONT_PATH = os.path.join("assets", "fonts", "Font.ttf")

class DialogBox:
    def __init__(self, font_size=24):
        # Cargar la fuente personalizada desde assets/fonts/Font.ttf
        try:
            self.font = pygame.font.Font(FONT_PATH, font_size)
        except pygame.error as e:
            print(f"⚠️ No se pudo cargar la fuente en {FONT_PATH}: {e}")
            # Fallback a una fuente del sistema si falla
            self.font = pygame.font.SysFont("Arial", font_size)

        # Dimensiones y posición del cuadro
        from settings import SCREEN_WIDTH, SCREEN_HEIGHT  # Importar solo lo necesario
        self.width = SCREEN_WIDTH // 1.25
        self.height = 160
        x = (SCREEN_WIDTH - self.width) // 2
        y = SCREEN_HEIGHT - self.height - 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.text = ""
        self.visible = False

        # Colores según la imagen (ajusta si la imagen tiene otros tonos)
        self.bg_color = (74, 85, 124)      # #4A557C
        self.border_color = (45, 55, 86)   # #2D3756
        self.border_radius = 15

    def set_text(self, text):
        self.text = text
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if not self.visible:
            return

        # Fondo redondeado
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)
        # Borde redondeado (más oscuro)
        pygame.draw.rect(screen, self.border_color, self.rect, width=3, border_radius=self.border_radius)

        # Renderizado del texto
        if self.text.strip():
            lines = self._split_text(self.text, self.width - 40)
            total_height = len(lines) * 30
            y_offset = self.rect.top + (self.height - total_height) // 2

            for line in lines:
                text_surface = self.font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(centerx=self.rect.centerx, top=y_offset)
                screen.blit(text_surface, text_rect)
                y_offset += 30

    def _split_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines