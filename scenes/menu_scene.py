# scenes/menu_scene.py
import pygame
import math
from settings import *

class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        # Cargar fondo
        self.background = pygame.image.load("assets/images/fondo.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Cargar y preparar el logo
        self.logo_original = pygame.image.load("assets/images/logo.png").convert_alpha()
        self.logo_rect = self.logo_original.get_rect(center=(SCREEN_WIDTH // 2, 120))

        # Cargar fuentes personalizadas
        try:
            self.font = pygame.font.Font("assets/fonts/Font.ttf", 64)
            self.small_font = pygame.font.Font("assets/fonts/Font.ttf", 36)
        except pygame.error as e:
            print(f"Error al cargar la fuente: {e}. Usando fuente predeterminada.")
            self.font = pygame.font.SysFont(None, 64)
            self.small_font = pygame.font.SysFont(None, 36)

        # Parámetros de animación
        self.start_time = pygame.time.get_ticks()
        self.anim_duration = 9000  # Duración total de un ciclo (expansión + retracción) en ms

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.running = False  # Sale del menú

    def update(self):
        # Calcular el progreso de la animación (ciclo senoidal suave)
        elapsed = pygame.time.get_ticks() - self.start_time
        cycle_progress = (elapsed % self.anim_duration) / self.anim_duration  # 0.0 a 1.0

        # Escalado senoidal: entre 0.9 y 1.1
        scale_factor = 0.9 + 0.2 * (math.sin(2 * math.pi * cycle_progress) + 1) / 2

        # Rotación ligera: entre -5 y +5 grados
        rotation_angle = 5 * math.sin(2 * math.pi * cycle_progress)

        # Escalar y rotar el logo
        scaled_logo = pygame.transform.scale_by(self.logo_original, scale_factor)
        rotated_logo = pygame.transform.rotate(scaled_logo, rotation_angle)
        self.logo_rect = rotated_logo.get_rect(center=(SCREEN_WIDTH // 2, 120))

        # Guardar la imagen rotada y escalada para dibujarla
        self.animated_logo = rotated_logo

    def draw(self):
        # Dibujar fondo
        self.screen.blit(self.background, (0, 0))

        # Dibujar logo animado
        self.screen.blit(self.animated_logo, self.logo_rect)

        # Renderizar texto con la fuente personalizada
        title = self.font.render("Pastel de Papa Salvamundos", True, WHITE)
        hint = self.small_font.render("Presiona ENTER para comenzar", True, LIGHT_YELLOW)

        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 400))

        pygame.display.flip()
