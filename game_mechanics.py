"""Kärnlogik för spelmekanik, fysik, AI och abilities."""

from __future__ import annotations

import math
from dataclasses import dataclass

import pygame

from characters import GODS, God
from settings import (
    GOAL_HEIGHT,
    GOAL_WIDTH,
    HEIGHT,
    MATCH_TIME_SECONDS,
    MAX_SCORE,
    PLAYER_RADIUS,
    PUCK_RADIUS,
    RINK_MARGIN,
    WIDTH,
)


@dataclass
class Effect:
    """Visuell effekt med enkel livslängd."""

    kind: str
    x: float
    y: float
    ttl: float


@dataclass
class Entity:
    """Basobjekt för spelare och puck."""

    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0


class GameState:
    """Innehåller all speldata och uppdateringsmetoder."""

    def __init__(self, selected_god: str) -> None:
        self.player_god: God = GODS[selected_god]
        self.ai_god: God = GODS["Ares"] if selected_god != "Ares" else GODS["Hermes"]

        self.player = Entity(x=WIDTH * 0.25, y=HEIGHT * 0.5)
        self.ai = Entity(x=WIDTH * 0.75, y=HEIGHT * 0.5)
        self.puck = Entity(x=WIDTH * 0.5, y=HEIGHT * 0.5)

        self.player_score = 0
        self.ai_score = 0
        self.time_left = float(MATCH_TIME_SECONDS)
        self.match_over = False

        self.effects: list[Effect] = []
        self.player_special_cd = 0.0
        self.player_temp_speed_bonus = 0.0
        self.player_temp_control = 1.0
        self.ai_slow_timer = 0.0
        self.lightning_active = 0.0

    def reset_positions(self) -> None:
        """Placera spelare och puck på standardpositioner efter mål."""
        self.player.x, self.player.y = WIDTH * 0.25, HEIGHT * 0.5
        self.ai.x, self.ai.y = WIDTH * 0.75, HEIGHT * 0.5
        self.puck.x, self.puck.y = WIDTH * 0.5, HEIGHT * 0.5
        self.puck.vx = 0
        self.puck.vy = 0

    def _rink_bounds(self) -> tuple[float, float, float, float]:
        return (RINK_MARGIN, RINK_MARGIN, WIDTH - RINK_MARGIN, HEIGHT - RINK_MARGIN)

    def _limit_entity(self, e: Entity, radius: int) -> None:
        left, top, right, bottom = self._rink_bounds()
        e.x = max(left + radius, min(right - radius, e.x))
        e.y = max(top + radius, min(bottom - radius, e.y))

    def _handle_puck_with_player(self) -> None:
        dx = self.puck.x - self.player.x
        dy = self.puck.y - self.player.y
        dist = math.hypot(dx, dy)
        touch_distance = PLAYER_RADIUS + PUCK_RADIUS + 3
        if dist < touch_distance and dist > 0:
            control = 2.5 * self.player_temp_control
            self.puck.vx += (dx / dist) * control
            self.puck.vy += (dy / dist) * control

    def _handle_puck_with_ai(self) -> None:
        dx = self.puck.x - self.ai.x
        dy = self.puck.y - self.ai.y
        dist = math.hypot(dx, dy)
        touch_distance = PLAYER_RADIUS + PUCK_RADIUS + 2
        if dist < touch_distance and dist > 0:
            self.puck.vx += (dx / dist) * 2.0
            self.puck.vy += (dy / dist) * 2.0

    def player_shoot(self) -> None:
        """Skjut puck om spelaren är nära."""
        dx = self.puck.x - self.player.x
        dy = self.puck.y - self.player.y
        dist = math.hypot(dx, dy)
        if dist <= PLAYER_RADIUS + PUCK_RADIUS + 18 and dist > 0:
            strength = self.player_god.shot_power
            if self.lightning_active > 0:
                strength *= 1.35
            self.puck.vx = (dx / dist) * strength
            self.puck.vy = (dy / dist) * strength

    def use_special(self) -> bool:
        """Aktivera spelarens unika ability. Returnerar True vid lyckad aktivering."""
        if self.player_special_cd > 0 or self.match_over:
            return False

        ability = self.player_god.ability
        if ability == "Lightning Shot":
            self.lightning_active = 2.2
            self.effects.append(Effect("lightning", self.player.x, self.player.y, 0.45))
        elif ability == "Ice Wave":
            self.ai_slow_timer = 3.0
            self.effects.append(Effect("ice_wave", self.player.x, self.player.y, 0.55))
        elif ability == "Tactical Pass":
            self.player_temp_control = 1.9
            self.effects.append(Effect("tactical", self.player.x, self.player.y, 0.6))
        elif ability == "War Dash":
            self.player.vx *= 2.8
            self.player.vy *= 2.8
            self.effects.append(Effect("dash", self.player.x, self.player.y, 0.35))
        elif ability == "Wind Sprint":
            self.player_temp_speed_bonus = 110.0
            self.effects.append(Effect("wind", self.player.x, self.player.y, 0.7))
        else:
            return False

        self.player_special_cd = self.player_god.special_cooldown
        return True

    def _update_timers(self, dt: float) -> None:
        self.player_special_cd = max(0.0, self.player_special_cd - dt)
        self.ai_slow_timer = max(0.0, self.ai_slow_timer - dt)
        self.lightning_active = max(0.0, self.lightning_active - dt)

        if self.player_temp_control > 1.0:
            self.player_temp_control = max(1.0, self.player_temp_control - dt * 0.45)
        if self.player_temp_speed_bonus > 0.0:
            self.player_temp_speed_bonus = max(0.0, self.player_temp_speed_bonus - dt * 60)

        for e in self.effects:
            e.ttl -= dt
        self.effects = [e for e in self.effects if e.ttl > 0]

    def _update_ai(self, dt: float) -> None:
        target_x, target_y = self.puck.x, self.puck.y
        to_x = target_x - self.ai.x
        to_y = target_y - self.ai.y
        dist = math.hypot(to_x, to_y) or 1.0

        ai_speed = self.ai_god.speed * (0.55 if self.ai_slow_timer > 0 else 1.0)
        self.ai.vx = (to_x / dist) * ai_speed
        self.ai.vy = (to_y / dist) * ai_speed

        self.ai.x += self.ai.vx * dt
        self.ai.y += self.ai.vy * dt
        self._limit_entity(self.ai, PLAYER_RADIUS)

        if dist < 120 and self.puck.x < self.ai.x:
            self.puck.vx -= 150 * dt

    def _update_puck(self, dt: float) -> None:
        self.puck.x += self.puck.vx * dt
        self.puck.y += self.puck.vy * dt

        self.puck.vx *= 0.992
        self.puck.vy *= 0.992

        left, top, right, bottom = self._rink_bounds()
        goal_top = HEIGHT * 0.5 - GOAL_HEIGHT * 0.5
        goal_bottom = goal_top + GOAL_HEIGHT

        in_goal_y = goal_top <= self.puck.y <= goal_bottom

        if self.puck.x - PUCK_RADIUS <= left and in_goal_y:
            self.ai_score += 1
            self.effects.append(Effect("goal", WIDTH * 0.5, HEIGHT * 0.5, 1.1))
            self.reset_positions()
        elif self.puck.x + PUCK_RADIUS >= right and in_goal_y:
            self.player_score += 1
            self.effects.append(Effect("goal", WIDTH * 0.5, HEIGHT * 0.5, 1.1))
            self.reset_positions()
        else:
            if self.puck.x - PUCK_RADIUS <= left:
                self.puck.x = left + PUCK_RADIUS
                self.puck.vx *= -0.9
            elif self.puck.x + PUCK_RADIUS >= right:
                self.puck.x = right - PUCK_RADIUS
                self.puck.vx *= -0.9

            if self.puck.y - PUCK_RADIUS <= top:
                self.puck.y = top + PUCK_RADIUS
                self.puck.vy *= -0.9
            elif self.puck.y + PUCK_RADIUS >= bottom:
                self.puck.y = bottom - PUCK_RADIUS
                self.puck.vy *= -0.9

    def update(self, dt: float, input_state) -> None:
        """Uppdatera hela game state per frame."""
        if self.match_over:
            return

        self.time_left = max(0.0, self.time_left - dt)
        if self.time_left <= 0 or self.player_score >= MAX_SCORE or self.ai_score >= MAX_SCORE:
            self.match_over = True

        move_len = math.hypot(input_state.move_x, input_state.move_y)
        if move_len > 0:
            nx = input_state.move_x / move_len
            ny = input_state.move_y / move_len
            speed = self.player_god.speed + self.player_temp_speed_bonus
            self.player.vx = nx * speed
            self.player.vy = ny * speed
        else:
            self.player.vx = 0
            self.player.vy = 0

        self.player.x += self.player.vx * dt
        self.player.y += self.player.vy * dt
        self._limit_entity(self.player, PLAYER_RADIUS)

        self._update_ai(dt)

        if input_state.shoot_pressed:
            self.player_shoot()

        self._handle_puck_with_player()
        self._handle_puck_with_ai()

        self._update_puck(dt)
        self._update_timers(dt)

    @property
    def winner_text(self) -> str:
        """Returnerar sluttext baserat på resultat."""
        if self.player_score > self.ai_score:
            return "DU VANN!"
        if self.player_score < self.ai_score:
            return "AI VANN"
        return "OAVGJORT"
