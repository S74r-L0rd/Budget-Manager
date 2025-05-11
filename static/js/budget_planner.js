export function setupBudgetFormToggle() {
  document.addEventListener("DOMContentLoaded", function () {
    const addBtn = document.getElementById("show-budget-form");
    const editLink = document.getElementById("edit-budget-plan");
    const formBlock = document.getElementById("budget-form-container");

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
  });
}