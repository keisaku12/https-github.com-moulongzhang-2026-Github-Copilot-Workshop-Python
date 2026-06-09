self.onmessage = (event) => {
  const { action, duration } = event.data;
  if (action === "start") {
    const startTime = Date.now();
    self.postMessage({ type: "started" });
    const intervalId = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      self.postMessage({ type: "tick", elapsed });
      if (elapsed >= duration) {
        clearInterval(intervalId);
        self.postMessage({ type: "finished" });
      }
    }, 1000);
  }
};
