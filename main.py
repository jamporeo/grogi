# main.py (actualizado)
import pygame
import os
import sys
from settings import *
from scenes.menu_scene import MenuScene
from scenes.intro_scene import IntroScene
from scenes.map_scene import MapScene

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pastel de Papa Salvamundos")
    clock = pygame.time.Clock()

    # Menú
    pygame.mixer.music.load(os.path.join(AUDIO_DIR, "Intro.mp3"))
    pygame.mixer.music.play(-1)
    menu = MenuScene(screen)
    while menu.running:
        events = pygame.event.get()
        menu.handle_events(events)
        menu.update()
        menu.draw()
        clock.tick(FPS)

    # Introducción
    intro = IntroScene(screen)
    while intro.running:
        events = pygame.event.get()
        intro.handle_events(events)
        intro.update()
        intro.draw()
        clock.tick(FPS)

    # Mapa principal
    map_scene = MapScene(screen)
    while map_scene.running:
        dt = clock.tick(FPS) / 1000.0  # Delta time en segundos
        events = pygame.event.get()
        map_scene.handle_events(events)
        map_scene.update(dt)
        map_scene.draw()

    # Aquí iría: cargar minijuego según map_scene.next_minigame
    print(f"Minijuego a cargar: {map_scene.next_minigame}")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()