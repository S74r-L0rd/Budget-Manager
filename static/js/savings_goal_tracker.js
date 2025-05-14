export function setupMultiUserSelector() {
  document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("user-multiselect");
    const dropdown = document.getElementById("dropdown-container");
    const selectedTags = document.getElementById("selected-tags");
    const hiddenInputs = document.getElementById("hidden-share-inputs");

    if (!container || !dropdown || !selectedTags || !hiddenInputs) return;

    // Toggle dropdown on click
    container.addEventListener("click", function (e) {
      if (!e.target.matches('input[type="checkbox"]')) {
        dropdown.classList.toggle("show");
      }
    });

    // Update selected tags and hidden inputs
    dropdown.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.addEventListener("change", function () {
        const userId = this.value;
        const userName = this.dataset.name;

        if (this.checked) {
          // Create tag
          const tag = document.createElement("span");
          tag.className = "tag";
          tag.textContent = userName;
          tag.dataset.id = userId;
          tag.addEventListener("click", () => {
            tag.remove();
            this.checked = false;
            hiddenInputs.querySelector(`input[value="${userId}"]`)?.remove();
          });
          selectedTags.appendChild(tag);

          // Create hidden input
          const hidden = document.createElement("input");
          hidden.type = "hidden";
          hidden.name = "share_with";
          hidden.value = userId;
          hiddenInputs.appendChild(hidden);
        } else {
          selectedTags.querySelector(`[data-id="${userId}"]`)?.remove();
          hiddenInputs.querySelector(`input[value="${userId}"]`)?.remove();
        }
      });
    });
  });
}