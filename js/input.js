export function createInput() {
  const down = new Set();
  const pressed = new Set();

  const onDown = (e) => {
    const key = e.key.toLowerCase();
    down.add(key);
    pressed.add(key);
  };
  const onUp = (e) => down.delete(e.key.toLowerCase());

  window.addEventListener('keydown', onDown);
  window.addEventListener('keyup', onUp);

  return {
    axis() {
      return {
        x: (down.has('d') || down.has('arrowright') ? 1 : 0) - (down.has('a') || down.has('arrowleft') ? 1 : 0),
        y: (down.has('s') || down.has('arrowdown') ? 1 : 0) - (down.has('w') || down.has('arrowup') ? 1 : 0),
      };
    },
    consume(key) {
      const ok = pressed.has(key);
      pressed.delete(key);
      return ok;
    },
    isDown(key) {
      return down.has(key);
    },
  };
}
