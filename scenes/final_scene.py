# scenes/final_scene.py
import pygame
import os
from settings import *

class FinalScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.result = None

        # === FONDO OBLIGATORIO ===
        fondo_path = os.path.join(IMAGES_DIR, "fondo_marmol.png")
        if os.path.exists(fondo_path):
            self.background = pygame.image.load(fondo_path).convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            # Si no está, falla con mensaje claro
            raise FileNotFoundError("❌ Falta el archivo: assets/images/fondo_marmol.png")

        # === FUENTE OBLIGATORIA ===
        font_path = os.path.join(FONTS_DIR, "Font.ttf")
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, 24)
            self.button_font = pygame.font.Font(font_path, 28)
        else:
            raise FileNotFoundError("❌ Falta el archivo: assets/fonts/Font.ttf")

        # === INGREDIENTES ===
        self.ingredients = [
            {"name": "papa", "state": "normal"},
            {"name": "queso", "state": "normal"},
            {"name": "carne", "state": "normal"}
        ]

        # === UTENSILIOS ===
        self.utensils = [
            {"name": "olla", "rect": None},
            {"name": "sarten", "rect": None},
            {"name": "cuchillo", "rect": None},
            {"name": "martillo", "rect": None}
        ]

        # === CARGAR SPRITES ===
        self.load_sprites()

        # Posiciones: izquierda (ingredientes), derecha (utensilios)
        self.ingredient_positions = [
            (100, 200),
            (100, 320),
            (100, 440)
        ]
        self.utensil_positions = [
            (SCREEN_WIDTH - 150, 200),
            (SCREEN_WIDTH - 150, 320),
            (SCREEN_WIDTH - 150, 440),
            (SCREEN_WIDTH - 150, 560)
        ]

        for i, pos in enumerate(self.ingredient_positions):
            self.ingredients[i]["pos"] = list(pos)

        for i, pos in enumerate(self.utensil_positions):
            self.utensils[i]["rect"] = pygame.Rect(pos[0], pos[1], 80, 80)

        # Arrastre
        self.dragging_ingredient = None
        self.drag_offset = (0, 0)

        # === BOTÓN OBLIGATORIO ===
        boton_path = os.path.join(IMAGES_DIR, "boton.png")
        if os.path.exists(boton_path):
            self.boton_img = pygame.image.load(boton_path).convert_alpha()
            self.boton_img = pygame.transform.scale(self.boton_img, (220, 70))
        else:
            raise FileNotFoundError("❌ Falta el archivo: assets/images/boton.png")

        self.boton_rect = self.boton_img.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))

        # Cuadro de diálogo simple (texto inferior)
        self.dialog_text = "Arrastra los ingredientes a los utensilios para prepararlos."
        self.dialog_bg = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH -175 , 100)

    def load_sprites(self):
        self.ingredient_sprites = {}
        self.utensil_sprites = {}

        # Ingredientes
        for base in ["papa", "queso", "carne"]:
            states = ["normal"]
            if base == "papa":
                states += ["cortada", "hervida", "pure"]
            elif base == "queso":
                states += ["cortado"]
            elif base == "carne":
                states += ["cocida"]

            self.ingredient_sprites[base] = {}
            for state in states:
                filename = f"{base}_{state}.png" if state != "normal" else f"icon_{base}.png"
                path = os.path.join(IMAGES_DIR, filename)
                if os.path.exists(path):
                    img = pygame.image.load(path).convert_alpha()
                    self.ingredient_sprites[base][state] = pygame.transform.scale(img, (80, 80))
                else:
                    surf = pygame.Surface((80, 80), pygame.SRCALPHA)
                    color_map = {"papa": (200, 150, 100), "queso": (255, 255, 150), "carne": (200, 50, 50)}
                    color = color_map.get(base, (150, 150, 150))
                    if state != "normal":
                        color = tuple(min(255, c + 30) for c in color)
                    pygame.draw.rect(surf, color, surf.get_rect())
                    text = self.font.render(f"{base[:3]}.{state[:4]}", True, (0, 0, 0))
                    surf.blit(text, (2, 2))
                    self.ingredient_sprites[base][state] = surf

        # Utensilios
        for tool in ["olla", "sarten", "cuchillo", "martillo"]:
            path = os.path.join(IMAGES_DIR, f"{tool}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.utensil_sprites[tool] = pygame.transform.scale(img, (80, 80))
            else:
                surf = pygame.Surface((80, 80))
                surf.fill((100, 100, 100))
                text = self.font.render(tool[:6], True, (255, 255, 255))
                surf.blit(text, (10, 30))
                self.utensil_sprites[tool] = surf

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.Vector2(event.pos)

                if self.boton_rect.collidepoint(mouse_pos):
                    self.check_final_result()
                    return

                for ing in self.ingredients:
                    rect = pygame.Rect(ing["pos"][0], ing["pos"][1], 80, 80)
                    if rect.collidepoint(mouse_pos):
                        self.dragging_ingredient = ing
                        self.drag_offset = (mouse_pos.x - ing["pos"][0], mouse_pos.y - ing["pos"][1])
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging_ingredient:
                    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                    ing = self.dragging_ingredient

                    for utensil in self.utensils:
                        if utensil["rect"].collidepoint(mouse_pos):
                            self.apply_utensil(ing, utensil["name"])
                            break
                    else:
                        idx = next(i for i, x in enumerate(self.ingredients) if x is ing)
                        ing["pos"] = list(self.ingredient_positions[idx])

                    self.dragging_ingredient = None

    def apply_utensil(self, ingredient, utensil_name):
        name = ingredient["name"]
        state = ingredient["state"]

        if name == "papa":
            if utensil_name == "cuchillo" and state == "normal":
                ingredient["state"] = "cortada"
            elif utensil_name == "olla" and state == "cortada":
                ingredient["state"] = "hervida"
            elif utensil_name == "martillo" and state == "hervida":
                ingredient["state"] = "pure"

        elif name == "queso":
            if utensil_name == "cuchillo" and state == "normal":
                ingredient["state"] = "cortado"

        elif name == "carne":
            if utensil_name == "sarten" and state == "normal":
                ingredient["state"] = "cocida"

        idx = next(i for i, x in enumerate(self.ingredients) if x is ingredient)
        ingredient["pos"] = list(self.ingredient_positions[idx])

    def check_final_result(self):
        papa_ok = False
        queso_ok = False
        carne_ok = False

        for ing in self.ingredients:
            if ing["name"] == "papa" and ing["state"] == "pure":
                papa_ok = True
            elif ing["name"] == "queso" and ing["state"] == "cortado":
                queso_ok = True
            elif ing["name"] == "carne" and ing["state"] == "cocida":
                carne_ok = True

        self.result = "good" if (papa_ok and queso_ok and carne_ok) else "bad"
        self.running = False

    def update(self, dt):
        if self.dragging_ingredient:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            self.dragging_ingredient["pos"] = [
                mouse_pos.x - self.drag_offset[0],
                mouse_pos.y - self.drag_offset[1]
            ]

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Utensilios (derecha)
        for utensil, pos in zip(self.utensils, self.utensil_positions):
            self.screen.blit(self.utensil_sprites[utensil["name"]], pos)

        # Ingredientes (izquierda + arrastre)
        for ing in self.ingredients:
            sprite = self.ingredient_sprites[ing["name"]][ing["state"]]
            self.screen.blit(sprite, ing["pos"])

        # Botón personalizado
        self.screen.blit(self.boton_img, self.boton_rect.topleft)

        # Texto en el botón
        btn_text = self.button_font.render("            ", True, (255, 255, 255))
        text_rect = btn_text.get_rect(center=self.boton_rect.center)
        self.screen.blit(btn_text, text_rect)

        # Cuadro de diálogo inferior
        pygame.draw.rect(self.screen, (30, 30, 30), self.dialog_bg)
        pygame.draw.line(self.screen, (100, 100, 100), (0, SCREEN_HEIGHT - 100), (SCREEN_WIDTH - 175, SCREEN_HEIGHT - 100), 2)
        dialog_surf = self.font.render(self.dialog_text, True, (220, 220, 200))
        self.screen.blit(dialog_surf, (20, SCREEN_HEIGHT - 70))

        pygame.display.flip()