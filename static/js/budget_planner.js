export function setupBudgetFormToggle() {
  document.addEventListener("DOMContentLoaded", function () {
    const addBtn = document.getElementById("show-budget-form");
    const editLink = document.getElementById("edit-budget-plan");
    const formBlock = document.getElementById("budget-form-container");

    // Budget form toggle
    function toggleForm(e) {
      e.preventDefault();
      if (formBlock) {
        formBlock.style.display = "block";
      }
      if (addBtn) addBtn.style.display = "none";
    }

    if (addBtn) {
      addBtn.addEventListener("click", toggleForm);
    }

    if (editLink) {
      editLink.addEventListener("click", toggleForm);
    }

    // Frequency switcher toggle
    const frequencyButtons = document.querySelectorAll("#frequency-toggle-group .tool-button");
    frequencyButtons.forEach(button => {
      button.addEventListener("click", function () {
        frequencyButtons.forEach(btn => btn.classList.remove("active"));
        this.classList.add("active");

        const selectedFrequency = this.getAttribute("data-frequency");
        console.log("User selected frequency:", selectedFrequency);

        // In future: Call chart update logic here using selectedFrequency
      });
    });
  });
}