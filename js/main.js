import { createAudio } from './audio.js';
import { createGame } from './game.js';
import { createInput } from './input.js';
import { draw } from './render.js';
import { HEIGHT, WIDTH } from './settings.js';
import { createTutorial } from './tutorial.js';
import { setupCharacterSelect, updateHud } from './ui.js';

const selectPanel = document.getElementById('select-panel');
const gamePanel = document.getElementById('game-panel');
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;

const input = createInput();
const audio = createAudio();

let game = null;
let tutorial = null;
let running = false;
let prevScore = '0-0';

setupCharacterSelect((godName) => {
  game = createGame(godName);
  tutorial = createTutorial();
  selectPanel.classList.add('hidden');
  gamePanel.classList.remove('hidden');
  running = true;
  prevScore = `${game.state.scoreP}-${game.state.scoreAI}`;
});

let last = performance.now();
function loop(now) {
  const dt = Math.min(0.033, (now - last) / 1000);
  last = now;

  if (running && game) {
    if (input.consume('r') && game.state.over) {
      game = createGame(game.state.playerGod.name);
      tutorial = createTutorial();
      prevScore = '0-0';
    }

    const didShoot = input.isDown(' ');
    const beforeCd = game.state.specialCd;
    game.step(dt, input);
    tutorial.update(dt, input, game);

    if (didShoot) audio.shoot();
    if (beforeCd === 0 && game.state.specialCd > 0) audio.special();

    const scoreNow = `${game.state.scoreP}-${game.state.scoreAI}`;
    if (scoreNow !== prevScore) {
      audio.goal();
      prevScore = scoreNow;
    }

    draw(ctx, game.state);
    updateHud(game.state, game.state.over ? `${game.state.scoreP > game.state.scoreAI ? 'DU VANN!' : game.state.scoreP < game.state.scoreAI ? 'AI VANN' : 'OAVGJORT'} · Tryck R för omstart` : tutorial.text());
  } else {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
  }

  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
