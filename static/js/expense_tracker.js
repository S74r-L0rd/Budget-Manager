export function scrollToElementSmoothly(id, offset = 150, duration = 600) {
  const target = document.getElementById(id);
  if (!target) return;

  const targetY = target.getBoundingClientRect().top + window.pageYOffset - offset;
  const startY = window.scrollY;
  const distance = targetY - startY;
  let startTime = null;

  function easeInOutQuad(t) {
    return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
  }

  function animateScroll(currentTime) {
    if (!startTime) startTime = currentTime;
    const timeElapsed = currentTime - startTime;
    const progress = easeInOutQuad(Math.min(timeElapsed / duration, 1));
    window.scrollTo(0, startY + distance * progress);
    if (timeElapsed < duration) {
      requestAnimationFrame(animateScroll);
    }
  }

  requestAnimationFrame(animateScroll);
}
