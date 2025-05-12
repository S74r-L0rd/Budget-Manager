export function scrollToElementSmoothly(id, offset = 750, duration = 600) {
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

// Main setup function
export function setupBudgetFormToggle() {
  document.addEventListener("DOMContentLoaded", function () {
    const addBtn = document.getElementById("show-budget-form");
    const editLink = document.getElementById("edit-budget-plan");
    const formBlock = document.getElementById("budget-form-container");

    // Toggle budget form
    function toggleForm(e) {
      e.preventDefault();
      if (formBlock) {
        formBlock.style.display = "block";
      }
      if (addBtn) addBtn.style.display = "none";
    }

    if (addBtn) addBtn.addEventListener("click", toggleForm);
    if (editLink) editLink.addEventListener("click", toggleForm);

    // Frequency switcher
    const frequencyButtons = document.querySelectorAll("#frequency-toggle-group .tool-button");
    frequencyButtons.forEach(button => {
      button.addEventListener("click", function () {
        frequencyButtons.forEach(btn => btn.classList.remove("active"));
        this.classList.add("active");

        const selectedFrequency = this.getAttribute("data-frequency");
        console.log("User selected frequency:", selectedFrequency);
      });
    });

    // Run smooth scroll if marker is present
    const scrollTarget = document.body.dataset.scrollTargetId;
    if (scrollTarget) {
      scrollToElementSmoothly(scrollTarget);
    }
  });
}