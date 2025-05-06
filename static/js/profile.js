// Function to preview image at the account setting page
function previewImage(event) {
    const image = document.getElementById('profile-img');
    image.src = URL.createObjectURL(event.target.files[0]);
  }

// Function to toggle between display and edit mode for each card
function toggleEdit(sectionId) {
    const displayEl = document.getElementById(sectionId + "-display");
    const editEl = document.getElementById(sectionId + "-edit");
    displayEl.classList.toggle("d-none");
    editEl.classList.toggle("d-none");
}

// Function to switch to the profile tab when clicking the cancel button in logout tab
function switchToProfile() {
    // Find the tab trigger element for #profile
    const triggerElement = document.querySelector('a[data-bs-toggle="list"][href="#profile"]');
    
    if (triggerElement) {
      const tab = new bootstrap.Tab(triggerElement);
      tab.show();
    }
  }