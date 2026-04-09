import { GODS } from './characters.js';

export function setupCharacterSelect(onStart) {
  const list = document.getElementById('god-list');
  const start = document.getElementById('start-btn');
  let selected = GODS[0].name;

  const render = () => {
    list.innerHTML = '';
    GODS.forEach((g) => {
      const card = document.createElement('button');
      card.className = `god-card ${selected === g.name ? 'active' : ''}`;
      card.innerHTML = `<strong style="color:${g.primary}">${g.name}</strong><br/>SPD ${g.speed}, SHOT ${g.shotPower}, CD ${g.cooldown}s<br/><small style="color:${g.accent}">${g.ability}</small>`;
      card.onclick = () => { selected = g.name; render(); };
      list.appendChild(card);
    });
  };

  start.onclick = () => onStart(selected);
  render();
}

export function updateHud(state, tutorialText) {
  document.getElementById('score').textContent = `Du ${state.scoreP} - ${state.scoreAI} AI`;
  document.getElementById('timer').textContent = `Tid: ${Math.floor(state.timeLeft)}`;
  document.getElementById('ability').textContent = `${state.playerGod.name} [${state.playerGod.ability}] CD: ${state.specialCd.toFixed(1)}s`;
  document.getElementById('tutorial').textContent = tutorialText;
}
