"""Entrypoint för Olympisk Gudahockey."""

import pygame

from audio import AudioManager
from characters import GOD_ORDER
from game_mechanics import GameState
from input_handler import read_input
from rendering import draw_effects, draw_entities, draw_rink
from settings import FPS, HEIGHT, WIDTH
from tutorial import Tutorial
from ui import draw_character_select, draw_end_overlay, draw_hud


def character_select(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    """Visar character-select och returnerar valt namn."""
    font = pygame.font.SysFont("consolas", 24)
    idx = 0

    while True:
        dt = clock.tick(FPS) / 1000.0
        _ = dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GOD_ORDER[0]
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    idx = (idx + 1) % len(GOD_ORDER)
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    idx = (idx - 1) % len(GOD_ORDER)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return GOD_ORDER[idx]

        draw_character_select(screen, font, idx)
        pygame.display.flip()


def run_game() -> None:
    """Startar och kör spelet fram till avslut."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Olympisk Gudahockey")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("consolas", 36, bold=True)
    ui_font = pygame.font.SysFont("consolas", 22)

    selected = character_select(screen, clock)
    game_state = GameState(selected)
    tutorial = Tutorial()
    audio = AudioManager()

    previous_player_score = 0
    previous_ai_score = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        events = pygame.event.get()
        input_state = read_input(events)

        if input_state.quit_pressed:
            running = False
            continue

        special_used = False
        if input_state.special_pressed:
            special_used = game_state.use_special()
            if special_used:
                audio.play_special()

        if input_state.shoot_pressed:
            audio.play_shoot()

        if input_state.restart_pressed and game_state.match_over:
            game_state = GameState(selected)
            tutorial = Tutorial()

        game_state.update(dt, input_state)
        tutorial.update(dt, input_state, game_state, special_used)

        if game_state.player_score != previous_player_score or game_state.ai_score != previous_ai_score:
            audio.play_goal()
            previous_player_score = game_state.player_score
            previous_ai_score = game_state.ai_score

        draw_rink(screen)
        draw_entities(screen, game_state)
        draw_effects(screen, game_state)
        draw_hud(screen, ui_font, game_state, tutorial.hint())

        if game_state.match_over:
            draw_end_overlay(screen, title_font, game_state.winner_text)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_game()
