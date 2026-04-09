"""Rendering av rink, sprites och effekter i retrostil."""

import pygame

from settings import (
    GOAL_HEIGHT,
    GOAL_WIDTH,
    HEIGHT,
    ICE_COLOR,
    LINE_COLOR,
    PLAYER_RADIUS,
    PUCK_RADIUS,
    RINK_MARGIN,
    TEAM_AI,
    TEAM_PLAYER,
    WIDTH,
)


def draw_rink(screen: pygame.Surface) -> None:
    """Rita hockeyrinken med retrofärger och enkla linjer."""
    screen.fill((8, 30, 58))
    rink = pygame.Rect(RINK_MARGIN, RINK_MARGIN, WIDTH - 2 * RINK_MARGIN, HEIGHT - 2 * RINK_MARGIN)
    pygame.draw.rect(screen, ICE_COLOR, rink)
    pygame.draw.rect(screen, LINE_COLOR, rink, 4)

    mid_x = WIDTH // 2
    pygame.draw.line(screen, LINE_COLOR, (mid_x, RINK_MARGIN), (mid_x, HEIGHT - RINK_MARGIN), 3)
    pygame.draw.circle(screen, LINE_COLOR, (mid_x, HEIGHT // 2), 56, 3)

    goal_y = HEIGHT // 2 - GOAL_HEIGHT // 2
    left_goal = pygame.Rect(RINK_MARGIN - GOAL_WIDTH, goal_y, GOAL_WIDTH, GOAL_HEIGHT)
    right_goal = pygame.Rect(WIDTH - RINK_MARGIN, goal_y, GOAL_WIDTH, GOAL_HEIGHT)
    pygame.draw.rect(screen, TEAM_AI, left_goal)
    pygame.draw.rect(screen, TEAM_PLAYER, right_goal)


def _draw_pixel_player(screen: pygame.Surface, x: float, y: float, color, accent) -> None:
    """Rita spelarsprite i pixel-blockstil."""
    body = pygame.Rect(int(x - PLAYER_RADIUS), int(y - PLAYER_RADIUS), PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)
    pygame.draw.rect(screen, color, body)
    pygame.draw.rect(screen, (20, 20, 20), body, 2)
    pygame.draw.rect(screen, accent, (body.x + 5, body.y + 4, body.w - 10, 7))
    pygame.draw.rect(screen, accent, (body.x + 6, body.y + body.h - 10, body.w - 12, 6))


def draw_entities(screen: pygame.Surface, game_state) -> None:
    """Rita spelare, AI och puck."""
    _draw_pixel_player(
        screen,
        game_state.player.x,
        game_state.player.y,
        game_state.player_god.primary_color,
        game_state.player_god.accent_color,
    )
    _draw_pixel_player(
        screen,
        game_state.ai.x,
        game_state.ai.y,
        game_state.ai_god.primary_color,
        game_state.ai_god.accent_color,
    )

    pygame.draw.circle(screen, (18, 18, 18), (int(game_state.puck.x), int(game_state.puck.y)), PUCK_RADIUS)
    pygame.draw.circle(screen, (255, 255, 255), (int(game_state.puck.x), int(game_state.puck.y)), PUCK_RADIUS, 1)


def draw_effects(screen: pygame.Surface, game_state) -> None:
    """Rita abilities/goal-effekter med enkla former."""
    for e in game_state.effects:
        if e.kind == "lightning":
            pts = [(e.x - 8, e.y - 22), (e.x + 4, e.y - 4), (e.x - 3, e.y - 4), (e.x + 8, e.y + 20)]
            pygame.draw.lines(screen, (255, 255, 120), False, pts, 4)
        elif e.kind == "ice_wave":
            pygame.draw.circle(screen, (150, 230, 255), (int(e.x), int(e.y)), int(40 * (1 - e.ttl / 0.55)) + 24, 3)
        elif e.kind == "tactical":
            pygame.draw.circle(screen, (210, 150, 255), (int(e.x), int(e.y)), 30, 2)
        elif e.kind == "dash":
            pygame.draw.line(screen, (255, 120, 120), (e.x - 25, e.y), (e.x + 25, e.y), 3)
        elif e.kind == "wind":
            pygame.draw.arc(screen, (190, 255, 230), (e.x - 30, e.y - 20, 60, 40), 0.2, 2.8, 3)
        elif e.kind == "goal":
            pygame.draw.circle(screen, (255, 255, 120), (int(e.x), int(e.y)), 72, 4)
