import { getGod } from './characters.js';
import { GOAL_HEIGHT, HEIGHT, MATCH_TIME, MAX_SCORE, PLAYER_RADIUS, PUCK_RADIUS, RINK_MARGIN, WIDTH } from './settings.js';

export function createGame(selectedGodName) {
  const playerGod = getGod(selectedGodName);
  const aiGod = getGod(selectedGodName === 'Ares' ? 'Hermes' : 'Ares');

  const state = {
    playerGod,
    aiGod,
    player: { x: WIDTH * 0.25, y: HEIGHT * 0.5, vx: 0, vy: 0 },
    ai: { x: WIDTH * 0.75, y: HEIGHT * 0.5, vx: 0, vy: 0 },
    puck: { x: WIDTH * 0.5, y: HEIGHT * 0.5, vx: 0, vy: 0 },
    scoreP: 0,
    scoreAI: 0,
    timeLeft: MATCH_TIME,
    over: false,
    specialCd: 0,
    effects: [],
    lightning: 0,
    aiSlow: 0,
    passBoost: 1,
    speedBoost: 0,
    goalFlash: 0,
  };

  const reset = () => {
    state.player.x = WIDTH * 0.25; state.player.y = HEIGHT * 0.5;
    state.ai.x = WIDTH * 0.75; state.ai.y = HEIGHT * 0.5;
    state.puck.x = WIDTH * 0.5; state.puck.y = HEIGHT * 0.5;
    state.puck.vx = 0; state.puck.vy = 0;
  };

  const clamp = (ent, r) => {
    ent.x = Math.max(RINK_MARGIN + r, Math.min(WIDTH - RINK_MARGIN - r, ent.x));
    ent.y = Math.max(RINK_MARGIN + r, Math.min(HEIGHT - RINK_MARGIN - r, ent.y));
  };

  const shoot = () => {
    const dx = state.puck.x - state.player.x;
    const dy = state.puck.y - state.player.y;
    const d = Math.hypot(dx, dy);
    if (d <= PLAYER_RADIUS + PUCK_RADIUS + 18 && d > 0) {
      const boost = state.lightning > 0 ? 1.35 : 1;
      const p = state.playerGod.shotPower * boost;
      state.puck.vx = (dx / d) * p;
      state.puck.vy = (dy / d) * p;
    }
  };

  const special = () => {
    if (state.specialCd > 0 || state.over) return false;
    switch (state.playerGod.ability) {
      case 'Lightning Shot': state.lightning = 2.2; break;
      case 'Ice Wave': state.aiSlow = 3; break;
      case 'Tactical Pass': state.passBoost = 1.9; break;
      case 'War Dash': state.player.vx *= 2.8; state.player.vy *= 2.8; break;
      case 'Wind Sprint': state.speedBoost = 110; break;
      default: return false;
    }
    state.effects.push({ kind: state.playerGod.ability, x: state.player.x, y: state.player.y, t: 0.65 });
    state.specialCd = state.playerGod.cooldown;
    return true;
  };

  const step = (dt, input) => {
    if (state.over) return;
    state.timeLeft = Math.max(0, state.timeLeft - dt);
    if (state.timeLeft === 0 || state.scoreP >= MAX_SCORE || state.scoreAI >= MAX_SCORE) state.over = true;

    const a = input.axis();
    const len = Math.hypot(a.x, a.y) || 1;
    const speed = state.playerGod.speed + state.speedBoost;
    state.player.vx = (a.x / len) * speed;
    state.player.vy = (a.y / len) * speed;
    if (a.x === 0 && a.y === 0) { state.player.vx = 0; state.player.vy = 0; }

    state.player.x += state.player.vx * dt;
    state.player.y += state.player.vy * dt;
    clamp(state.player, PLAYER_RADIUS);

    const tx = state.puck.x - state.ai.x;
    const ty = state.puck.y - state.ai.y;
    const td = Math.hypot(tx, ty) || 1;
    const aiSpeed = state.aiGod.speed * (state.aiSlow > 0 ? 0.55 : 1);
    state.ai.vx = (tx / td) * aiSpeed;
    state.ai.vy = (ty / td) * aiSpeed;
    state.ai.x += state.ai.vx * dt;
    state.ai.y += state.ai.vy * dt;
    clamp(state.ai, PLAYER_RADIUS);

    if (input.consume(' ')) shoot();

    if (input.consume('e')) state.lastSpecial = special();
    else state.lastSpecial = false;

    const touch = (actor, mult) => {
      const dx = state.puck.x - actor.x;
      const dy = state.puck.y - actor.y;
      const d = Math.hypot(dx, dy);
      if (d < PLAYER_RADIUS + PUCK_RADIUS + 3 && d > 0) {
        state.puck.vx += (dx / d) * mult;
        state.puck.vy += (dy / d) * mult;
      }
    };
    touch(state.player, 2.5 * state.passBoost);
    touch(state.ai, 2.0);

    state.puck.x += state.puck.vx * dt;
    state.puck.y += state.puck.vy * dt;
    state.puck.vx *= 0.992;
    state.puck.vy *= 0.992;

    const gt = HEIGHT * 0.5 - GOAL_HEIGHT * 0.5;
    const gb = gt + GOAL_HEIGHT;
    const inGoal = state.puck.y >= gt && state.puck.y <= gb;

    if (state.puck.x - PUCK_RADIUS <= RINK_MARGIN && inGoal) {
      state.scoreAI += 1; state.goalFlash = 0.9; reset();
    } else if (state.puck.x + PUCK_RADIUS >= WIDTH - RINK_MARGIN && inGoal) {
      state.scoreP += 1; state.goalFlash = 0.9; reset();
    } else {
      if (state.puck.x - PUCK_RADIUS <= RINK_MARGIN || state.puck.x + PUCK_RADIUS >= WIDTH - RINK_MARGIN) state.puck.vx *= -0.9;
      if (state.puck.y - PUCK_RADIUS <= RINK_MARGIN || state.puck.y + PUCK_RADIUS >= HEIGHT - RINK_MARGIN) state.puck.vy *= -0.9;
      clamp(state.puck, PUCK_RADIUS);
    }

    state.specialCd = Math.max(0, state.specialCd - dt);
    state.lightning = Math.max(0, state.lightning - dt);
    state.aiSlow = Math.max(0, state.aiSlow - dt);
    state.passBoost = Math.max(1, state.passBoost - dt * 0.45);
    state.speedBoost = Math.max(0, state.speedBoost - dt * 60);
    state.goalFlash = Math.max(0, state.goalFlash - dt);

    state.effects.forEach((e) => (e.t -= dt));
    state.effects = state.effects.filter((e) => e.t > 0);
  };

  return { state, step, reset, special };
}
