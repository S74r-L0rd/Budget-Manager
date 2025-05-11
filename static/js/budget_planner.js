export function setupBudgetFormToggle() {
  document.addEventListener("DOMContentLoaded", function () {
    const triggerBtn = document.getElementById("show-budget-form");
    const formBlock = document.getElementById("budget-form-container");

    if (triggerBtn && formBlock) {
      triggerBtn.addEventListener("click", function (e) {
        e.preventDefault();
        formBlock.style.display = "block";
        triggerBtn.style.display = "none";
      });
    }
  });
}