"""UI-ritning för HUD, menyer och texter."""

import pygame

from characters import GOD_ORDER, GODS
from settings import HEIGHT, UI_PANEL, WHITE, WIDTH


def draw_character_select(screen: pygame.Surface, font: pygame.font.Font, index: int) -> None:
    """Visa enkel character select innan matchstart."""
    screen.fill((12, 19, 35))
    title = font.render("Välj olympisk gud (A/D, Enter)", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))

    for i, name in enumerate(GOD_ORDER):
        god = GODS[name]
        color = god.primary_color
        y = 160 + i * 60
        marker = ">" if i == index else " "
        text = font.render(
            f"{marker} {god.name}: SPD {int(god.speed)} SHOT {int(god.shot_power)} CD {god.special_cooldown:.1f}s",
            True,
            color,
        )
        screen.blit(text, (140, y))

        ability = font.render(f"   Ability: {god.ability}", True, god.accent_color)
        screen.blit(ability, (150, y + 26))


def draw_hud(screen: pygame.Surface, small_font: pygame.font.Font, game_state, tutorial_text: str) -> None:
    """Rita score, timer, cooldown och tutorial-hints."""
    panel = pygame.Rect(0, 0, WIDTH, 44)
    pygame.draw.rect(screen, UI_PANEL, panel)

    timer_txt = small_font.render(f"Tid: {int(game_state.time_left)}", True, WHITE)
    score_txt = small_font.render(f"Du {game_state.player_score} - {game_state.ai_score} AI", True, WHITE)
    ability_txt = small_font.render(
        f"{game_state.player_god.name} [{game_state.player_god.ability}] CD: {game_state.player_special_cd:.1f}s",
        True,
        game_state.player_god.accent_color,
    )

    screen.blit(timer_txt, (18, 11))
    screen.blit(score_txt, (150, 11))
    screen.blit(ability_txt, (340, 11))

    hint_bg = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)
    pygame.draw.rect(screen, UI_PANEL, hint_bg)
    hint_txt = small_font.render(tutorial_text, True, WHITE)
    screen.blit(hint_txt, (18, HEIGHT - 28))


def draw_end_overlay(screen: pygame.Surface, font: pygame.font.Font, message: str) -> None:
    """Visa overlay när matchen är slut."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    msg = font.render(message, True, WHITE)
    hint = font.render("Tryck R för att starta om, ESC för att avsluta", True, WHITE)

    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 15))
