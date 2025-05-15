document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("user-multiselect");
    const dropdown = document.getElementById("dropdown-container");
    const selectedTags = document.getElementById("selected-tags");
    const hiddenInputs = document.getElementById("hidden-share-inputs");

    if (!container || !dropdown || !selectedTags || !hiddenInputs) return;

    // Toggle dropdown visibility on click
    container.addEventListener("click", function (e) {
        if (!e.target.matches('input[type="checkbox"]')) {
            dropdown.classList.toggle("show");
        }
    });

    // Hide dropdown when clicking outside
    document.addEventListener("click", function (e) {
        if (!container.contains(e.target)) {
            dropdown.classList.remove("show");
        }
    });

    // Handle user selection and deselection
    dropdown.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            const userId = this.value;
            const userName = this.dataset.name;

            if (this.checked) {
                // Add tag and hidden input
                addTag(userId, userName);
                addHiddenInput(userId);
            } else {
                // Remove tag and hidden input
                removeTag(userId);
                removeHiddenInput(userId);
            }
        });
    });

    function addTag(userId, userName) {
        const tag = document.createElement("span");
        tag.className = "tag badge bg-primary text-white me-1";
        tag.textContent = userName;
        tag.dataset.id = userId;
        tag.addEventListener("click", function () {
            removeTag(userId);
            removeHiddenInput(userId);
            dropdown.querySelector(`input[value="${userId}"]`).checked = false;
        });
        selectedTags.appendChild(tag);
    }

    function removeTag(userId) {
        const tag = selectedTags.querySelector(`[data-id="${userId}"]`);
        if (tag) tag.remove();
    }

    function addHiddenInput(userId) {
        const hidden = document.createElement("input");
        hidden.type = "hidden";
        hidden.name = "share_with";
        hidden.value = userId;
        hiddenInputs.appendChild(hidden);
    }

    function removeHiddenInput(userId) {
        const hidden = hiddenInputs.querySelector(`input[value="${userId}"]`);
        if (hidden) hidden.remove();
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // Automatically close flash messages after 4 seconds (4000 milliseconds)
    setTimeout(function() {
        const flashContainer = document.getElementById("flash-container");
        if (flashContainer) {
            flashContainer.classList.add("fade-out");
            setTimeout(() => flashContainer.remove(), 1000); // Remove after fade-out
        }
    }, 4000);
    // Fade-out CSS effect
    const style = document.createElement('style');
    style.innerHTML = `
    .fade-out {
        opacity: 0;
        transition: opacity 1s ease-out;
    }
    `;
    document.head.appendChild(style);

    // Show Delete Account Modal
    function showDeleteAccountModal() {
        const deleteModal = new bootstrap.Modal(document.getElementById("deleteAccountModal"));
        deleteModal.show();
    }
});


  
