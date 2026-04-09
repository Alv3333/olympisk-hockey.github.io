
# Olympisk Gudahockey (statiskt för GitHub Pages)

Detta projekt är nu ett **helt statiskt** 2D retro-hockeyspel byggt med **HTML, CSS och vanilla JavaScript (Canvas)**, så det fungerar direkt i **GitHub Pages** utan serverkod.

## Funktioner

- Top-down 2D hockey i pixel/16-bit-inspirerad stil
- Spelbara olympiska gudar med stats och unika abilities:
  - Zeus: Lightning Shot
  - Poseidon: Ice Wave
  - Athena: Tactical Pass
  - Ares: War Dash
  - Hermes: Wind Sprint
- WASD-rörelse, skott (Space), special (E), restart (R)
- AI-motståndare, score, matchtimer och HUD
- Interaktiv tutorial i tre steg
- Enkla retro-ljudeffekter via WebAudio API

## Kör lokalt

Du kan öppna `index.html` direkt i en webbläsare, eller köra en enkel lokal statisk server:

```bash
python -m http.server 8000
```

Öppna sedan: `http://localhost:8000`

## GitHub Pages

1. Pusha repot till GitHub.
2. Gå till **Settings → Pages**.
3. Välj **Deploy from a branch**.
4. Välj branch (t.ex. `main`) och root (`/`).
5. Spara. Spelet körs från `index.html`.

## Projektstruktur

- `index.html` – markup och paneler (character select + game)
- `styles.css` – retroinspirerad styling
- `js/main.js` – game loop och wiring
- `js/game.js` – spelmekanik, fysik, AI, mål, abilities
- `js/render.js` – rendering av rink, sprites, effekter
- `js/input.js` – tangentinput
- `js/ui.js` – character select och HUD
- `js/tutorial.js` – interaktiv tutorial
- `js/audio.js` – retro-ljud via oscillatorer
- `js/characters.js` – guddata och stats
- `js/settings.js` – konstanter
- 
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

