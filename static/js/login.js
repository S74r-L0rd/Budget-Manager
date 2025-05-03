// Add forgot password and return to login functionality
document.addEventListener("DOMContentLoaded", function () {
    // Handle tab switching for login and signup
    const loginTab = document.getElementById("login-tab");
    const signupTab = document.getElementById("signup-tab");
// get all flash messages
const flashMessages = document.querySelectorAll('.alert');
        
// set 5 seconds to auto dismiss
flashMessages.forEach(function(alert) {
  setTimeout(function() {
    // use Bootstrap's alert dismiss function
    const closeButton = new bootstrap.Alert(alert);
    closeButton.close();
  }, 5000); // 5000 milliseconds = 5 seconds
});


    loginTab.addEventListener("click", function () {
      hideAllForms();
      document.getElementById("login-form").classList.add("show", "active");
      resetTabStatus();
      loginTab.classList.add("active");
      loginTab.setAttribute("aria-selected", "true");
    });

    signupTab.addEventListener("click", function () {
      hideAllForms();
      document
        .getElementById("signup-form")
        .classList.add("show", "active");
      resetTabStatus();
      signupTab.classList.add("active");
      signupTab.setAttribute("aria-selected", "true");
    });

    // Forgot password link click event
    document
      .getElementById("forgotPasswordLink")
      .addEventListener("click", function () {
        hideAllForms();
        document
          .getElementById("forgot-password-form")
          .classList.add("show", "active");
        resetTabStatus();
      });

    // Back to login link click event
    document
      .getElementById("backToLogin")
      .addEventListener("click", function () {
        hideAllForms();
        document
          .getElementById("login-form")
          .classList.add("show", "active");
        resetTabStatus();
        loginTab.classList.add("active");
        loginTab.setAttribute("aria-selected", "true");
      });

    // Helper functions
    function hideAllForms() {
      document.querySelectorAll(".tab-pane").forEach(function (tabPane) {
        tabPane.classList.remove("show", "active");
      });
    }

    function resetTabStatus() {
      document.querySelectorAll(".nav-link").forEach(function (navLink) {
        navLink.classList.remove("active");
        navLink.setAttribute("aria-selected", "false");
      });
    }
  });

// Password visibility toggle function
function togglePasswordVisibility(inputId) {
  const passwordInput = document.getElementById(inputId);
  const toggleButton = passwordInput.nextElementSibling;
  const toggleIcon = toggleButton.querySelector('i');
  
  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    toggleIcon.classList.remove('bi-eye-slash');
    toggleIcon.classList.add('bi-eye');
  } else {
    passwordInput.type = 'password';
    toggleIcon.classList.remove('bi-eye');
    toggleIcon.classList.add('bi-eye-slash');
  }
}