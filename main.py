# main.py
import pygame
import os
import sys
from settings import *
from scenes.menu_scene import MenuScene
from scenes.intro_scene import IntroScene
from scenes.map_scene import MapScene
from scenes.puzzle_papa import PapaPuzzleScene
from scenes.puzzle_carne import CarnePuzzleScene
from scenes.puzzle_queso import QuesoPuzzleScene
from scenes.final_scene import FinalScene  # ← Importación añadida
from scenes.good_ending import GoodEndingScene  # ← AÑADIDO
from scenes.bad_ending import BadEndingScene   # ← AÑADIDO

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pastel de Papa")
    clock = pygame.time.Clock()

    # === MENÚ ===
    pygame.mixer.music.load(os.path.join(AUDIO_DIR, "intro.mp3"))
    pygame.mixer.music.play(-1)
    menu = MenuScene(screen)
    while menu.running:
        events = pygame.event.get()
        menu.handle_events(events)
        menu.update()
        menu.draw()
        clock.tick(FPS)

    # === INTRODUCCIÓN ===
    intro = IntroScene(screen)
    while intro.running:
        events = pygame.event.get()
        intro.handle_events(events)
        intro.update()
        intro.draw()
        clock.tick(FPS)

    # === INVENTARIO ===
    inventory = {
        "papa": False,
        "carne": False,
        "queso": False
    }

    # === CICLO PRINCIPAL: MAPA + MINIJUEGOS ===
    run_game = True
    while run_game:
        # Verificar si ya tiene los 3 ingredientes → ir al final
        if inventory["papa"] and inventory["carne"] and inventory["queso"]:
            final_scene = FinalScene(screen)
            while final_scene.running:
                dt = clock.tick(FPS) / 1000.0
                events = pygame.event.get()
                final_scene.handle_events(events)
                final_scene.update(dt)
                final_scene.draw()
            
            # === AÑADIDO: Escenas de final según resultado ===
            if final_scene.result == "good":
                ending = GoodEndingScene(screen)
                while ending.running:
                    events = pygame.event.get()
                    ending.handle_events(events)
                    ending.update()
                    ending.draw()
            else:
                ending = BadEndingScene(screen)
                while ending.running:
                    events = pygame.event.get()
                    ending.handle_events(events)
                    ending.update()
                    ending.draw()
            # ===============================================
            
            break  # Termina el juego tras la escena final

        # Crear nueva escena de mapa con estado actualizado
        map_scene = MapScene(screen)
        for item in inventory:
            map_scene.zones[item]["completed"] = inventory[item]

        # Ejecutar el mapa
        while map_scene.running:
            dt = clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            map_scene.handle_events(events)
            map_scene.update(dt)
            map_scene.draw()

        # Verificar si se seleccionó un minijuego
        if hasattr(map_scene, 'next_minigame'):
            minigame_name = map_scene.next_minigame

            if minigame_name == "papa" and not inventory["papa"]:
                puzzle = PapaPuzzleScene(screen)
                while puzzle.running:
                    dt = clock.tick(FPS) / 1000.0
                    events = pygame.event.get()
                    puzzle.handle_events(events)
                    puzzle.update(dt)
                    puzzle.draw()
                inventory["papa"] = True

            elif minigame_name == "carne" and not inventory["carne"]:
                puzzle = CarnePuzzleScene(screen)
                while puzzle.running:
                    dt = clock.tick(FPS) / 1000.0
                    events = pygame.event.get()
                    puzzle.handle_events(events)
                    puzzle.update(dt)
                    puzzle.draw()
                inventory["carne"] = True

            elif minigame_name == "queso" and not inventory["queso"]:
                puzzle = QuesoPuzzleScene(screen)
                while puzzle.running:
                    dt = clock.tick(FPS) / 1000.0
                    events = pygame.event.get()
                    puzzle.handle_events(events)
                    puzzle.update(dt)
                    puzzle.draw()
                inventory["queso"] = True

            # Si ya está completado, vuelve al mapa (sin hacer nada)

        else:
            # El jugador cerró la ventana desde el mapa
            run_game = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
