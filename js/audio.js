export function createAudio() {
  let ctx = null;
  const ensure = () => {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    return ctx;
  };

  const beep = (freq, ms) => {
    const a = ensure();
    const o = a.createOscillator();
    const g = a.createGain();
    o.frequency.value = freq;
    o.type = 'square';
    g.gain.value = 0.05;
    o.connect(g);
    g.connect(a.destination);
    o.start();
    o.stop(a.currentTime + ms / 1000);
  };

  return {
    shoot: () => beep(660, 90),
    special: () => beep(440, 140),
    goal: () => beep(880, 200),
  };
}
