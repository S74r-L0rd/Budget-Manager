export function scrollToPredictionWithOffset() {
  const OFFSET = 150; // Adjust for your fixed header height if any
  const target = document.querySelector('#prediction-result');

  if (target) {
    // Delay to ensure DOM and layout are fully rendered
    setTimeout(() => {
      const targetTop = target.getBoundingClientRect().top + window.scrollY - OFFSET;
      window.scrollTo({ top: targetTop, behavior: 'smooth' });

    }, 300);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  scrollToPredictionWithOffset();
});