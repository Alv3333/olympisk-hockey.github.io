export function createTutorial() {
  const steps = ['Rör dig med WASD', 'Skjut pucken med Space', 'Använd special med E'];
  return {
    idx: 0,
    moveTime: 0,
    done: false,
    update(dt, input, game) {
      if (this.done) return;
      if (this.idx === 0) {
        const a = input.axis();
        if (a.x !== 0 || a.y !== 0) this.moveTime += dt;
        if (this.moveTime >= 0.8) this.idx++;
      } else if (this.idx === 1 && input.isDown(' ')) this.idx++;
      else if (this.idx === 2 && game.state.lastSpecial) this.idx++;
      if (this.idx >= steps.length) this.done = true;
    },
    text() {
      return this.done ? 'Tutorial klar! Spela matchen.' : `Tutorial: ${steps[this.idx]}`;
    },
  };
}
