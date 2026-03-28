# scenes/puzzle_queso.py
import pygame
import os
from settings import *
from engine.dialog_box import DialogBox
from narrative.scripts import NARRATOR_VOICES

class QuesoPuzzleScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.solved = False
        self.win_time = None

        # Fondo
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((255, 250, 200))  # Amarillo claro (queso)

        # Terminales
        self.terminal_a = pygame.Rect(200, SCREEN_HEIGHT // 2 - 25, 50, 50)
        self.terminal_b = pygame.Rect(SCREEN_WIDTH - 250, SCREEN_HEIGHT // 2 - 25, 50, 50)

        self.dragging = False
        self.drag_start = None
        self.drag_end = None

        self.dialog_box = DialogBox()
        self.dialog_box.set_text("Conecta el cable desde la Terminal A hasta la Terminal B para enfriar el queso.")

        # Fanfarria
        self.fanfare_path = os.path.join(AUDIO_DIR, "Fanfare.mp3")
        self.fanfare_loaded = os.path.exists(self.fanfare_path)

        pygame.mixer.music.pause()

        # Música del minijuego
        minigame_music_path = os.path.join(AUDIO_DIR, "minigame.mp3")
        if os.path.exists(minigame_music_path):
            pygame.mixer.music.load(minigame_music_path)
            pygame.mixer.music.play(-1)  # Loop indefinidamente
        else:
            print(f"[WARNING] Música del minijuego no encontrada: {minigame_music_path}")

    def handle_events(self, events):
        if self.solved:
            return

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.Vector2(event.pos)
                if self.terminal_a.collidepoint(mouse_pos):
                    self.dragging = True
                    self.drag_start = (self.terminal_a.centerx, self.terminal_a.centery)
                    self.drag_end = mouse_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                    self.dragging = False
                    self.drag_end = mouse_pos

                    # Verificar si soltó sobre Terminal B
                    if self.terminal_b.collidepoint(mouse_pos):
                        self.solved = True
                        self.win_time = pygame.time.get_ticks()
                        self.dialog_box.set_text(NARRATOR_VOICES["queso"])
                        if self.fanfare_loaded:
                            pygame.mixer.music.load(self.fanfare_path)
                            pygame.mixer.music.play()
                    else:
                        self.dialog_box.set_text("¡Fallaste! Conecta el cable directamente a la Terminal B.")

    def update(self, dt):
        if self.dragging:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            self.drag_end = mouse_pos

        if self.solved:
            current_time = pygame.time.get_ticks()
            if current_time - self.win_time >= 3000:
                pygame.mixer.music.stop()
                self.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Dibujar terminales
        pygame.draw.rect(self.screen, (100, 100, 100), self.terminal_a)
        pygame.draw.rect(self.screen, (100, 100, 100), self.terminal_b)
        pygame.draw.rect(self.screen, (255, 255, 255), self.terminal_a, 2)
        pygame.draw.rect(self.screen, (255, 255, 255), self.terminal_b, 2)

        # Etiquetas
        font = pygame.font.SysFont(None, 36)
        text_a = font.render("A", True, (255, 255, 255))
        text_b = font.render("B", True, (255, 255, 255))
        self.screen.blit(text_a, (self.terminal_a.centerx - 12, self.terminal_a.centery - 18))
        self.screen.blit(text_b, (self.terminal_b.centerx - 12, self.terminal_b.centery - 18))

        # Dibujar cable (si se está arrastrando)
        if self.dragging and self.drag_start and self.drag_end:
            pygame.draw.line(self.screen, (0, 0, 255), self.drag_start, self.drag_end, 4)

        # Instrucción
        hint_font = pygame.font.SysFont(None, 28)
        hint = hint_font.render("Haz clic en A, arrastra hasta B y suelta.", True, (100, 100, 0))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 100))

        self.dialog_box.draw(self.screen)
        pygame.display.flip()