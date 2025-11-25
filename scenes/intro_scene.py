# scenes/intro_scene.py
import pygame
import os
from settings import *
from engine.dialog_box import DialogBox
from narrative.scripts import INTRO_DIALOGUE, VOICES

class IntroScene:
    def __init__(self, screen):
        self.screen = screen
        self.dialog_box = DialogBox()
        self.background = pygame.image.load(os.path.join(IMAGES_DIR, "intro_background.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Cargar personajes (opcional, si tienes sprites)
        self.char1 = None  # Narrador
        self.char2 = None  # Zoóloga
        try:
            self.char2 = pygame.image.load(os.path.join(IMAGES_DIR, "character2.png")).convert_alpha()
        except:
            pass  # Si no hay imagen, sigue sin problema
        

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

        # Aquí podrías reproducir sonido según el hablante
        if dialog["speaker"] == "Zoóloga":
            sound_file = os.path.join(AUDIO_DIR, VOICES.get("Zoologa", ""))
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

        # Dibujar personaje (opcional)
        if self.char2:
            self.screen.blit(self.char2, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 300))

        self.dialog_box.draw(self.screen)

        pygame.display.flip()