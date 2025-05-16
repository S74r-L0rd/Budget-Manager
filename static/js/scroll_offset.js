document.addEventListener('DOMContentLoaded', function () {
  const OFFSET = 190; // Adjust this to match your fixed header height
  const hash = window.location.hash;

  if (hash) {
    const target = document.querySelector(hash);
    if (target) {
      setTimeout(() => {
        const topOffset = target.getBoundingClientRect().top + window.scrollY - OFFSET;
        window.scrollTo({ top: topOffset, behavior: 'smooth' });
      }, 200); // Delay to ensure rendering
    }
  }
});