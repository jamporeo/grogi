# scenes/puzzle_papa.py
import pygame
import os
from settings import *
from engine.dialog_box import DialogBox
from narrative.scripts import PAPA_RIDDLE

class PapaPuzzleScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.solved = False

        # Cargar fuente personalizada solo para elementos dibujados aquí
        font_path = os.path.join(FONTS_DIR, "Font.ttf")
        try:
            self.font = pygame.font.Font(font_path, 36)
            self.hint_font = pygame.font.Font(font_path, 28)
        except:
            print("Advertencia: no se pudo cargar la fuente personalizada. Usando SysFont.")
            self.font = pygame.font.SysFont(None, 36)
            self.hint_font = pygame.font.SysFont(None, 28)

        # Cargar fondo de imagen
        background_path = os.path.join(IMAGES_DIR, "papa_fondo.png")
        try:
            self.background = pygame.image.load(background_path).convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print("Advertencia: no se pudo cargar 'papa_fondo.png'. Usando color de respaldo.")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((30, 50, 30))

        # Icono del papá
        try:
            self.papa_icon = pygame.image.load(os.path.join(IMAGES_DIR, "icon_papa.png")).convert_alpha()
            self.papa_icon = pygame.transform.scale(self.papa_icon, (150, 150))
        except:
            self.papa_icon = None

        # DialogBox SIN pasarle 'font' (como estaba originalmente)
        self.dialog_box = DialogBox(font_size=28)
        self.dialog_box.set_text(PAPA_RIDDLE["question"])

        self.options = PAPA_RIDDLE["options"]
        self.correct = PAPA_RIDDLE["correct"]

        # Para manejar el tiempo de salida
        self.exit_time = None

        # Cargar y reproducir fanfarria
        fanfare_path = os.path.join(AUDIO_DIR, "Fanfare.mp3")
        if os.path.exists(fanfare_path):
            try:
                pygame.mixer.music.load(fanfare_path)
                self.fanfare_duration = 3000
                self.use_fanfare = True
            except:
                self.use_fanfare = False
        else:
            self.use_fanfare = False

        pygame.mixer.music.pause()

        # Música del minijuego
        minigame_music_path = os.path.join(AUDIO_DIR, "minigame.mp3")
        if os.path.exists(minigame_music_path):
            pygame.mixer.music.load(minigame_music_path)
            pygame.mixer.music.play(-1)  # Loop indefinidamente
        else:
            print(f"[WARNING] Música del minijuego no encontrada: {minigame_music_path}")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and not self.solved:
                if event.key == pygame.K_a:
                    self.check_answer(0)
                elif event.key == pygame.K_b:
                    self.check_answer(1)
                elif event.key == pygame.K_c:
                    self.check_answer(2)

    def check_answer(self, choice):
        if choice == self.correct:
            self.solved = True
            self.dialog_box.set_text(PAPA_RIDDLE["success_message"])
            if self.use_fanfare:
                pygame.mixer.music.play()
                self.exit_time = pygame.time.get_ticks() + self.fanfare_duration
            else:
                self.exit_time = pygame.time.get_ticks() + 2000
        else:
            self.dialog_box.set_text(PAPA_RIDDLE["failure_message"])

    def update(self, dt):
        if self.solved and self.exit_time is not None:
            if pygame.time.get_ticks() >= self.exit_time:
                pygame.mixer.music.stop()
                self.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if self.papa_icon:
            self.screen.blit(self.papa_icon, (SCREEN_WIDTH // 2 - 75, 80))

        y_start = 300
        for i, option in enumerate(self.options):
            color = (100, 255, 100) if self.solved and i == self.correct else WHITE
            text = self.font.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_start + i * 50))

        hint = self.hint_font.render("Presiona A, B o C para responder", True, LIGHT_YELLOW)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, y_start + 180))

        self.dialog_box.draw(self.screen)
        pygame.display.flip()