export const GODS = [
  { name: 'Zeus', speed: 215, shotPower: 520, cooldown: 7, ability: 'Lightning Shot', primary: '#ffd166', accent: '#ffffff' },
  { name: 'Poseidon', speed: 205, shotPower: 460, cooldown: 8, ability: 'Ice Wave', primary: '#118ab2', accent: '#b9ecff' },
  { name: 'Athena', speed: 220, shotPower: 445, cooldown: 6.5, ability: 'Tactical Pass', primary: '#8338ec', accent: '#d2b4ff' },
  { name: 'Ares', speed: 210, shotPower: 500, cooldown: 7.5, ability: 'War Dash', primary: '#e63946', accent: '#ffb3b3' },
  { name: 'Hermes', speed: 235, shotPower: 430, cooldown: 6, ability: 'Wind Sprint', primary: '#06d6a0', accent: '#d8fff3' },
];

export function getGod(name) {
  return GODS.find((g) => g.name === name) ?? GODS[0];
}
