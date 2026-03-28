# scenes/intro_scene.py
import pygame
import os
from settings import *
from engine.dialog_box import DialogBox
from narrative.scripts import INTRO_DIALOGUE  # Solo INTRO_DIALOGUE

class IntroScene:
    def __init__(self, screen):
        self.screen = screen
        self.dialog_box = DialogBox()
        self.background = pygame.image.load(os.path.join(IMAGES_DIR, "intro_background.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Cargar personaje (opcional)
        self.char2 = None
        char_path = os.path.join(IMAGES_DIR, "character2.png")
        if os.path.exists(char_path):
            self.char2 = pygame.image.load(char_path).convert_alpha()

        self.dialog_index = 0
        self.waiting_for_input = True
        self.running = True
        self.load_next_dialog()

    def load_next_dialog(self):
        if self.dialog_index >= len(INTRO_DIALOGUE):
            self.running = False
            return

        dialog = INTRO_DIALOGUE[self.dialog_index]
        self.dialog_box.set_text(dialog["text"])
        self.current_speaker = dialog["speaker"]
        self.waiting_for_input = True

        # Reproducir sonido si es la Zoóloga
        if dialog["speaker"] == "Zoóloga":
            sound_file = os.path.join(AUDIO_DIR, "Voz_Zoologa.ogg")
            if not os.path.exists(sound_file):
                sound_file = os.path.join(AUDIO_DIR, "Voz_Zoologa.wav")
            if os.path.exists(sound_file):
                pygame.mixer.Sound(sound_file).play()
        if dialog["speaker"] == "Mecánica":
            sound_file = os.path.join(AUDIO_DIR, "Voz_Mecanica.ogg")
            if not os.path.exists(sound_file):
                sound_file = os.path.join(AUDIO_DIR, "Voz_Mecanica.wav")
            if os.path.exists(sound_file):
                pygame.mixer.Sound(sound_file).play()
        if dialog["speaker"] == "Steampunker":
            sound_file = os.path.join(AUDIO_DIR, "Voz_Steampunker.ogg")
            if not os.path.exists(sound_file):
                sound_file = os.path.join(AUDIO_DIR, "Voz_Steampunker.wav")
            if os.path.exists(sound_file):
                pygame.mixer.Sound(sound_file).play()
        if dialog["speaker"] == "Narrador":
            sound_file = os.path.join(AUDIO_DIR, "Voz_Narrador.ogg")
            if not os.path.exists(sound_file):
                sound_file = os.path.join(AUDIO_DIR, "Voz_Narrador.wav")
            if os.path.exists(sound_file):
                pygame.mixer.Sound(sound_file).play()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and self.waiting_for_input:
                if event.key == pygame.K_SPACE:
                    self.dialog_index += 1
                    self.load_next_dialog()

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if self.char2:
            self.screen.blit(self.char2, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 300))

        self.dialog_box.draw(self.screen)
        pygame.display.flip()