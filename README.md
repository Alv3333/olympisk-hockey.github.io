# Olympisk Gudahockey (Python + Pygame)

Ett komplett 2D retro-hockeyspel i pixelart/16-bit-stil där du spelar som olympiska gudar.

## Funktioner

- Top-down 2D hockey med puck, mål, timer och poäng
- Spelbara gudar med unika sprites, stats och abilities:
  - **Zeus**: Lightning Shot (snabbare puck + blixt)
  - **Poseidon**: Ice Wave (saktar motståndare)
  - **Athena**: Tactical Pass (bättre puckkontroll)
  - **Ares**: War Dash (kort dash för snabb förflyttning)
  - **Hermes**: Wind Sprint (temporär speed boost)
- Interaktiv tutorial:
  - Rörelse (WASD)
  - Skott (Space)
  - Special ability (E)
- AI-motståndare
- Moduler för input, rendering, spelmekanik, UI och audio

## Installera

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Kör spelet

```bash
python main.py
```

## Kontroller

- **WASD**: rörelse
- **Space**: skott
- **E**: special ability
- **R**: starta om match
- **Esc**: avsluta

## Projektstruktur

- `main.py` – spel-loop och skärmhantering
- `settings.py` – konstanter
- `characters.py` – gudar, stats och abilities
- `input_handler.py` – tangentbordsinput
- `game_mechanics.py` – spelobjekt, fysik, AI och regler
- `tutorial.py` – interaktiv tutorial-logik
- `rendering.py` – rendering av plan, spelare, puck, effekter
- `ui.py` – HUD, timer, hints och menyer
- `audio.py` – enkel retro-audio (toner via pygame.mixer)

## Notering

Alla sprites är pixelart-liknande och genereras programmatiskt för att hålla projektet självbärande utan externa assets.
