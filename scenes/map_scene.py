# scenes/map_scene.py
import pygame
import os
from settings import *
from engine.dialog_box import DialogBox


class MapScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        self.background = pygame.image.load(os.path.join(IMAGES_DIR, "map_background.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.load_player_sprites()

        self.player_pos = pygame.Vector2(100, SCREEN_HEIGHT - 150)
        self.target_pos = self.player_pos.copy()
        self.moving = False
        self.speed = 200

        self.facing_right = True
        self.current_sprite = self.idle_right

        # Para la animación de caminata
        self.walk_frame = 0
        self.walk_timer = 0
        self.walk_frame_duration = 0.175  # segundos por frame

        try:
            self.walk_sound = pygame.mixer.Sound(os.path.join(AUDIO_DIR, "walk.wav"))
            self.walk_sound.set_volume(0.4)
        except:
            self.walk_sound = None

        self.zones = {
            "papa": {
                "rect": pygame.Rect(230, 470, 100, 100),
                "completed": False,
                "icon": pygame.image.load(os.path.join(IMAGES_DIR, "icon_papa.png")).convert_alpha()
            },
            "carne": {
                "rect": pygame.Rect(500, 350, 100, 100),
                "completed": False,
                "icon": pygame.image.load(os.path.join(IMAGES_DIR, "icon_carne.png")).convert_alpha()
            },
            "queso": {  # ← Cambiado de "verduras" a "queso"
                "rect": pygame.Rect(705, 430, 100, 100),  # ← Misma posición que antes
                "completed": False,
                "icon": pygame.image.load(os.path.join(IMAGES_DIR, "icon_queso.png")).convert_alpha()  # ← Nuevo ícono
            },
        }

        for zone in self.zones.values():
            zone["icon"] = pygame.transform.scale(zone["icon"], (80, 80))

        self.dialog_box = DialogBox()
        self.show_hint = False
        self.hint_timer = 0

        try:
            pygame.mixer.music.load(os.path.join(AUDIO_DIR, "Musica.mp3"))
            pygame.mixer.music.play(-1)
        except:
            pass

    def load_player_sprites(self):
        def load_or_default(filename, size=(60, 80)):
            path = os.path.join(IMAGES_DIR, filename)
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, size)
            else:
                surf = pygame.Surface(size, pygame.SRCALPHA)
                color = (255, 0, 0) if "Izquierda" in filename else (0, 0, 255)
                pygame.draw.rect(surf, color, surf.get_rect())
                return surf

        self.walk_right = load_or_default("Caminar_Derecha.png")
        self.idle_right = load_or_default("Quieta_Derecha.png")
        self.walk_left = load_or_default("Caminar_Izquierda.png")
        self.idle_left = load_or_default("Quieta_Izquierda.png")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.Vector2(event.pos)

                # Mensajes amigables actualizados
                NICE_NAMES = {"papa": "papas", "carne": "carne molida", "queso": "queso"}

                for name, zone in self.zones.items():
                    if zone["rect"].collidepoint(mouse_pos):
                        if not zone["completed"]:
                            self.start_minigame(name)
                        else:
                            self.dialog_box.set_text(f"Ya tienes {NICE_NAMES.get(name, name)}.")
                            self.show_hint = True
                            self.hint_timer = 0
                        return

                self.target_pos = mouse_pos.copy()
                self.moving = True
                self.facing_right = self.target_pos.x > self.player_pos.x
                if self.walk_sound and not pygame.mixer.get_busy():
                    self.walk_sound.play()

    def start_minigame(self, zone_name):
        self.running = False
        self.next_minigame = zone_name

    def update(self, dt):
        if self.moving:
            direction = self.target_pos - self.player_pos
            distance = direction.length()
            if distance > 0:
                direction.normalize_ip()
                movement = direction * self.speed * dt
                if movement.length() >= distance:
                    self.player_pos = self.target_pos.copy()
                    self.moving = False
                    self.current_sprite = self.idle_right if self.facing_right else self.idle_left
                else:
                    self.player_pos += movement

                    # Animación de caminata: alternar entre caminar y quieto
                    self.walk_timer += dt
                    if self.walk_timer >= self.walk_frame_duration:
                        self.walk_timer = 0
                        self.walk_frame = (self.walk_frame + 1) % 2  # 0 o 1

                    if self.walk_frame == 0:
                        self.current_sprite = self.walk_right if self.facing_right else self.walk_left
                    else:
                        self.current_sprite = self.idle_right if self.facing_right else self.idle_left
            else:
                self.moving = False
                self.current_sprite = self.idle_right if self.facing_right else self.idle_left
        else:
            self.current_sprite = self.idle_right if self.facing_right else self.idle_left

        if self.show_hint:
            self.hint_timer += dt
            if self.hint_timer > 2.0:
                self.dialog_box.hide()
                self.show_hint = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for zone in self.zones.values():
            pygame.draw.rect(self.screen, (50, 50, 50), zone["rect"], 2)
            icon_rect = zone["icon"].get_rect(center=zone["rect"].center)
            self.screen.blit(zone["icon"], icon_rect)

        player_rect = self.current_sprite.get_rect(midbottom=(int(self.player_pos.x), int(self.player_pos.y)))
        self.screen.blit(self.current_sprite, player_rect)

        self.dialog_box.draw(self.screen)
        pygame.display.flip()