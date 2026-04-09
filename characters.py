"""Karaktärsdefinitioner och ability-konfiguration."""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class God:
    """Representerar en spelbar gud med stats och specialförmåga."""

    name: str
    speed: float
    shot_power: float
    special_cooldown: float
    ability: str
    primary_color: Tuple[int, int, int]
    accent_color: Tuple[int, int, int]


GODS: Dict[str, God] = {
    "Zeus": God(
        name="Zeus",
        speed=215,
        shot_power=520,
        special_cooldown=7.0,
        ability="Lightning Shot",
        primary_color=(255, 209, 102),
        accent_color=(255, 255, 255),
    ),
    "Poseidon": God(
        name="Poseidon",
        speed=205,
        shot_power=460,
        special_cooldown=8.0,
        ability="Ice Wave",
        primary_color=(17, 138, 178),
        accent_color=(154, 214, 255),
    ),
    "Athena": God(
        name="Athena",
        speed=220,
        shot_power=445,
        special_cooldown=6.5,
        ability="Tactical Pass",
        primary_color=(131, 56, 236),
        accent_color=(224, 170, 255),
    ),
    "Ares": God(
        name="Ares",
        speed=210,
        shot_power=500,
        special_cooldown=7.5,
        ability="War Dash",
        primary_color=(230, 57, 70),
        accent_color=(255, 173, 173),
    ),
    "Hermes": God(
        name="Hermes",
        speed=235,
        shot_power=430,
        special_cooldown=6.0,
        ability="Wind Sprint",
        primary_color=(6, 214, 160),
        accent_color=(207, 255, 244),
    ),
}

GOD_ORDER = list(GODS.keys())
