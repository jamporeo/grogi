# main.py (actualizado)
import pygame
import os
import sys
from settings import *
from scenes.menu_scene import MenuScene
from scenes.intro_scene import IntroScene
from scenes.map_scene import MapScene
from scenes.puzzle_papa import PapaPuzzleScene

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

    # Estado del inventario (compartido)
    inventory = {
        "papa": False,
        "carne": False,
        "verduras": False
    }

    run_map = True
    while run_map:
        map_scene = MapScene(screen)
        # Restaurar estado del inventario en las zonas
        for item in inventory:
            map_scene.zones[item]["completed"] = inventory[item]

        # Ejecutar mapa
        while map_scene.running:
            dt = clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            map_scene.handle_events(events)
            map_scene.update(dt)
            map_scene.draw()

        # ¿Qué minijuego se debe cargar?
        if hasattr(map_scene, 'next_minigame'):
            minigame_name = map_scene.next_minigame

            if minigame_name == "papa" and not inventory["papa"]:
                puzzle = PapaPuzzleScene(screen)
                # En el bucle del minijuego
                while puzzle.running:
                    dt = clock.tick(FPS) / 1000.0
                    events = pygame.event.get()
                    puzzle.handle_events(events)
                    puzzle.update(dt)  # ← ahora recibe dt
                    puzzle.draw()
                # Marcar como completado
                inventory["papa"] = True

            # Aquí irán los otros minijuegos más adelante
            else:
                # Si ya está resuelto, volver al mapa
                pass

        else:
            run_map = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()