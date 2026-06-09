export function formatTime(seconds) {
  const minutes = String(Math.floor(seconds / 60)).padStart(2, "0");
  const secs = String(seconds % 60).padStart(2, "0");
  return `${minutes}:${secs}`;
}

export function createTimer(durationSeconds) {
  let remaining = durationSeconds;
  let running = false;
  let lastTick = Date.now();

  const tick = () => {
    if (!running) return;
    const now = Date.now();
    const diff = Math.floor((now - lastTick) / 1000);
    if (diff > 0) {
      remaining = Math.max(0, remaining - diff);
      lastTick = now;
    }
  };

  return {
    start() {
      if (!running) {
        running = true;
        lastTick = Date.now();
      }
    },
    stop() {
      running = false;
    },
    reset(value) {
      remaining = value;
      lastTick = Date.now();
    },
    update() {
      tick();
      return remaining;
    },
    isRunning() {
      return running;
    },
  };
}
