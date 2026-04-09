import { GOAL_HEIGHT, HEIGHT, PLAYER_RADIUS, PUCK_RADIUS, RINK_MARGIN, WIDTH } from './settings.js';

export function draw(ctx, state) {
  ctx.clearRect(0, 0, WIDTH, HEIGHT);
  ctx.fillStyle = '#08203e';
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  ctx.fillStyle = '#bce4ff';
  ctx.fillRect(RINK_MARGIN, RINK_MARGIN, WIDTH - 2 * RINK_MARGIN, HEIGHT - 2 * RINK_MARGIN);

  ctx.strokeStyle = '#db2640';
  ctx.lineWidth = 4;
  ctx.strokeRect(RINK_MARGIN, RINK_MARGIN, WIDTH - 2 * RINK_MARGIN, HEIGHT - 2 * RINK_MARGIN);
  ctx.beginPath();
  ctx.moveTo(WIDTH / 2, RINK_MARGIN);
  ctx.lineTo(WIDTH / 2, HEIGHT - RINK_MARGIN);
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(WIDTH / 2, HEIGHT / 2, 56, 0, Math.PI * 2);
  ctx.stroke();

  const gy = HEIGHT / 2 - GOAL_HEIGHT / 2;
  ctx.fillStyle = '#ef476f';
  ctx.fillRect(RINK_MARGIN - 14, gy, 14, GOAL_HEIGHT);
  ctx.fillStyle = '#ffd60a';
  ctx.fillRect(WIDTH - RINK_MARGIN, gy, 14, GOAL_HEIGHT);

  drawPlayer(ctx, state.player, state.playerGod.primary, state.playerGod.accent);
  drawPlayer(ctx, state.ai, state.aiGod.primary, state.aiGod.accent);

  ctx.fillStyle = '#111';
  ctx.beginPath();
  ctx.arc(state.puck.x, state.puck.y, PUCK_RADIUS, 0, Math.PI * 2);
  ctx.fill();

  drawEffects(ctx, state);
}

function drawPlayer(ctx, p, color, accent) {
  ctx.fillStyle = color;
  ctx.fillRect(p.x - PLAYER_RADIUS, p.y - PLAYER_RADIUS, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2);
  ctx.strokeStyle = '#111';
  ctx.strokeRect(p.x - PLAYER_RADIUS, p.y - PLAYER_RADIUS, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2);
  ctx.fillStyle = accent;
  ctx.fillRect(p.x - PLAYER_RADIUS + 5, p.y - PLAYER_RADIUS + 4, PLAYER_RADIUS * 2 - 10, 7);
}

function drawEffects(ctx, state) {
  state.effects.forEach((e) => {
    if (e.kind === 'Lightning Shot') {
      ctx.strokeStyle = '#ffff99';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(e.x - 8, e.y - 20); ctx.lineTo(e.x + 2, e.y - 2); ctx.lineTo(e.x - 4, e.y - 2); ctx.lineTo(e.x + 8, e.y + 22);
      ctx.stroke();
    }
    if (e.kind === 'Ice Wave') {
      ctx.strokeStyle = '#b8f1ff';
      ctx.beginPath();
      ctx.arc(e.x, e.y, 24 + (1 - e.t) * 36, 0, Math.PI * 2);
      ctx.stroke();
    }
    if (e.kind === 'Tactical Pass') {
      ctx.strokeStyle = '#d9b8ff';
      ctx.beginPath();
      ctx.arc(e.x, e.y, 32, 0, Math.PI * 2);
      ctx.stroke();
    }
  });

  if (state.goalFlash > 0) {
    ctx.strokeStyle = `rgba(255,255,120,${state.goalFlash})`;
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.arc(WIDTH / 2, HEIGHT / 2, 74, 0, Math.PI * 2);
    ctx.stroke();
  }
}
