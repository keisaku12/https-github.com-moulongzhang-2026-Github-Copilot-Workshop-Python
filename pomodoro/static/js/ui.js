import { formatTime, createTimer } from "./timerEngine.js";

const durationSeconds = 25 * 60;
const timer = createTimer(durationSeconds);
const timerElement = document.querySelector(".timer");
const startButton = document.getElementById("start-button");
const resetButton = document.getElementById("reset-button");

function render() {
  const remaining = timer.update();
  timerElement.textContent = formatTime(remaining);
}

startButton.addEventListener("click", () => {
  if (timer.isRunning()) {
    timer.stop();
    startButton.textContent = "開始";
  } else {
    timer.start();
    startButton.textContent = "一時停止";
  }
});

resetButton.addEventListener("click", () => {
  timer.reset(durationSeconds);
  timer.stop();
  startButton.textContent = "開始";
  render();
});

setInterval(render, 1000);
render();
