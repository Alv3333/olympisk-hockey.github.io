"""Enkel retro-audio med genererade toner."""

from __future__ import annotations

import array
import math

import pygame


class AudioManager:
    """Skapar och spelar upp enkla ljudeffekter i runtime."""

    def __init__(self) -> None:
        self.enabled = True
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.shoot = self._tone(660, 0.08)
            self.special = self._tone(440, 0.15)
            self.goal = self._tone(880, 0.2)
        except pygame.error:
            self.enabled = False

    def _tone(self, frequency: int, duration: float, volume: float = 0.35) -> pygame.mixer.Sound:
        """Generera enkel sinus-ton som pygame Sound."""
        sample_rate = 22050
        num_samples = int(duration * sample_rate)
        buf = array.array("h")
        amp = int(32767 * volume)
        for n in range(num_samples):
            value = int(amp * math.sin(2 * math.pi * frequency * (n / sample_rate)))
            buf.append(value)
        return pygame.mixer.Sound(buffer=buf)

    def play_shoot(self) -> None:
        if self.enabled:
            self.shoot.play()

    def play_special(self) -> None:
        if self.enabled:
            self.special.play()

    def play_goal(self) -> None:
        if self.enabled:
            self.goal.play()
