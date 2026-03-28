# scenes/puzzle_carne.py
import pygame
import os
from settings import *
from engine.dialog_box import DialogBox
from narrative.scripts import NARRATOR_VOICES

class CarnePuzzleScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.solved = False
        self.win_time = None  # Momento en que se resolvió

        # Cargar fondo personalizado
        fondo_path = os.path.join(IMAGES_DIR, "carne_fondo.png")
        if os.path.exists(fondo_path):
            self.background = pygame.image.load(fondo_path)
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            print(f"[WARNING] Fondo no encontrado: {fondo_path}. Usando color de respaldo.")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((80, 40, 40))  # Rojo oscuro como respaldo

        # Cargar fuente personalizada
        font_path = os.path.join(FONTS_DIR, "Font.ttf")
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, 28)
            self.small_font = pygame.font.Font(font_path, 24)
            self.debug_font = pygame.font.Font(font_path, 48)
        else:
            print(f"[WARNING] Fuente no encontrada: {font_path}. Usando SysFont.")
            self.font = pygame.font.SysFont(None, 28)
            self.small_font = pygame.font.SysFont(None, 24)
            self.debug_font = pygame.font.SysFont(None, 48)

        # Cargar piezas
        self.pieces = []
        for i in range(4):
            path = os.path.join(IMAGES_DIR, f"carne_pieza_{i}.png")
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path)
                    scaled_img = pygame.transform.scale(img, (100, 100))
                    final_img = scaled_img.convert_alpha() if img.get_alpha() is not None else scaled_img.convert()
                    self.pieces.append(final_img)
                except Exception as e:
                    print(f"[ERROR] No se pudo cargar {path}: {e}")
                    self.pieces.append(self.create_debug_piece(i))
            else:
                print(f"[WARNING] Archivo no encontrado: {path}")
                self.pieces.append(self.create_debug_piece(i))

        # Tablero central
        board_x = SCREEN_WIDTH // 2 - 110
        board_y = SCREEN_HEIGHT // 2 - 60
        self.board_slots = [
            pygame.Rect(board_x, board_y, 100, 100),
            pygame.Rect(board_x + 120, board_y, 100, 100),
            pygame.Rect(board_x, board_y + 120, 100, 100),
            pygame.Rect(board_x + 120, board_y + 120, 100, 100)
        ]

        # Posiciones iniciales
        left_x = SCREEN_WIDTH // 2 - 300
        right_x = SCREEN_WIDTH // 2 + 150
        y0 = SCREEN_HEIGHT // 2 - 100
        y1 = SCREEN_HEIGHT // 2 + 20
        self.initial_positions = [
            (left_x, y0),
            (left_x, y1),
            (right_x, y0),
            (right_x, y1)
        ]
        self.piece_positions = [pos for pos in self.initial_positions]
        self.dragging_piece = None
        self.drag_offset = (0, 0)

        self.dialog_box = DialogBox()
        self.dialog_box.set_text("Arrastra las piezas a los espacios correctos para reconstruir la carne molida.")

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

    def create_debug_piece(self, index):
        surf = pygame.Surface((100, 100))
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
        surf.fill(colors[index])
        pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), 3)
        text = self.debug_font.render(str(index), True, (0, 0, 0))
        surf.blit(text, (38, 25))
        return surf

    def handle_events(self, events):
        if self.solved:
            return  # No procesar eventos mientras se muestra la fanfarria

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.Vector2(event.pos)
                for i in range(4):
                    piece_rect = pygame.Rect(self.piece_positions[i], (100, 100))
                    if piece_rect.collidepoint(mouse_pos):
                        self.dragging_piece = i
                        self.drag_offset = (mouse_pos.x - self.piece_positions[i][0],
                                            mouse_pos.y - self.piece_positions[i][1])
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging_piece is not None:
                    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                    piece_id = self.dragging_piece
                    placed = False
                    for slot_rect in self.board_slots:
                        if slot_rect.collidepoint(mouse_pos):
                            self.piece_positions[piece_id] = slot_rect.topleft
                            placed = True
                            break
                    if not placed:
                        self.piece_positions[piece_id] = self.initial_positions[piece_id]
                    self.dragging_piece = None
                    self.check_win()

    def check_win(self):
        correct = True
        for slot_idx in range(4):
            if self.piece_positions[slot_idx] != self.board_slots[slot_idx].topleft:
                correct = False
                break
        if correct:
            self.solved = True
            self.win_time = pygame.time.get_ticks()
            self.dialog_box.set_text(NARRATOR_VOICES["carne"])
            if self.fanfare_loaded:
                pygame.mixer.music.load(self.fanfare_path)
                pygame.mixer.music.play()

    def update(self, dt):
        # Actualizar arrastre
        if self.dragging_piece is not None and not self.solved:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            new_x = mouse_pos.x - self.drag_offset[0]
            new_y = mouse_pos.y - self.drag_offset[1]
            self.piece_positions[self.dragging_piece] = (new_x, new_y)

        # Verificar si ya pasaron 3 segundos tras resolver
        if self.solved:
            current_time = pygame.time.get_ticks()
            if current_time - self.win_time >= 3000:
                pygame.mixer.music.stop()
                self.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Dibujar slots del tablero
        for i, rect in enumerate(self.board_slots):
            pygame.draw.rect(self.screen, (60, 60, 60), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            text = self.small_font.render(str(i), True, (200, 200, 200))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        # Dibujar piezas
        for i in range(4):
            self.screen.blit(self.pieces[i], self.piece_positions[i])
            if self.dragging_piece == i:
                pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(self.piece_positions[i], (100, 100)), 3)

        # Instrucción
        hint = self.font.render("Haz clic y arrastra las piezas al tablero.", True, (255, 255, 150))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 100))

        self.dialog_box.draw(self.screen)
        pygame.display.flip()