document.addEventListener("DOMContentLoaded", function () {
  const countdown = document.getElementById("countdown");
  if (!countdown) return;

  let counter = 5;
  const interval = setInterval(() => {
    counter--;
    countdown.textContent = counter;
    if (counter === 0) {
      clearInterval(interval);
      window.location.href = countdown.dataset.redirect;
    }
  }, 1000);
});