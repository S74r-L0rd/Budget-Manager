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

// Function to handle tab switching
document.addEventListener('DOMContentLoaded', function() {
  const accountSettingTab = document.getElementById('account-setting-tab');
  accountSettingTab.addEventListener('click', function() {
      document.querySelectorAll('.tab-pane').forEach(tab => tab.classList.remove('show', 'active'));
      document.getElementById('account-setting').classList.add('show', 'active');
  });
});

// Function to check if the new password and confirm password fields match
document.addEventListener('DOMContentLoaded', function () {
    const newPassword = document.getElementById('newPassword');
    const confirmPassword = document.getElementById('confirmPassword');
    const passwordError = document.getElementById('passwordError');

    confirmPassword.addEventListener('input', function () {
        if (newPassword.value !== confirmPassword.value) {
            passwordError.textContent = "Passwords do not match!";
        } else {
            passwordError.textContent = "";
        }
    });
});

// Function to dismiss flash messgaes after 2 seconds
document.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {
      var alertElement = document.querySelector('.alert');
      if (alertElement) {
          var bsAlert = new bootstrap.Alert(alertElement);
          bsAlert.close();
      }
  }, 2000); // Dismiss after 2 seconds
});


// Show Change Password Modal
function showChangePasswordModal() {
  const changePasswordModal = new bootstrap.Modal(document.getElementById("passwordModal"));
  changePasswordModal.show();
}

// Show Delete Account Modal
function showDeleteAccountModal() {
  const deleteModal = new bootstrap.Modal(document.getElementById("deleteAccountModal"));
  deleteModal.show();
}