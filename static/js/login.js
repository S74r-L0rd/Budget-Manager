// Add forgot password and return to login functionality
document.addEventListener("DOMContentLoaded", function () {
    // Handle tab switching for login and signup
    const loginTab = document.getElementById("login-tab");
    const signupTab = document.getElementById("signup-tab");
    const forgotPasswordLink = document.getElementById("forgotPasswordLink");
    const backToLogin = document.getElementById("backToLogin");

    // get all flash messages
    const flashMessages = document.querySelectorAll('.alert');
    
    // check if there is a clear form mark
    let shouldClearSignupForm = false;
    let shouldClearForgotForm = false;
    
    flashMessages.forEach(function(alert) {
      // check flash message category
      if (alert.classList.contains('alert-clear_form')) {
        const message = alert.textContent.trim();
        if (message === 'clear_signup_form') {
          shouldClearSignupForm = true;
          // hide this special message
          dismissAlert(alert);
        } else if (message === 'clear_forgot_form') {
          shouldClearForgotForm = true;
          // hide this special message
          dismissAlert(alert);
        }
      }
      
      // set 5 seconds to auto dismiss
      setTimeout(function() {
        dismissAlert(alert);
      }, 5000); // 5000 milliseconds = 5 seconds
    });
    
    // if need to clear signup form
    if (shouldClearSignupForm) {
      clearSignupForm();
      // ensure signup form is active
      if (!document.getElementById("signup-form").classList.contains('active')) {
        signupTab.click();
      }
    }
    
    // if need to clear forgot password form
    if (shouldClearForgotForm) {
      clearForgotPasswordForm();
      // ensure forgot password form is active
      if (!document.getElementById("forgot-password-form").classList.contains('active')) {
        forgotPasswordLink.click();
      }
    }
            
    // Function to dismiss flash messages
    function dismissAllAlerts() {
      const currentAlerts = document.querySelectorAll('.alert');
      currentAlerts.forEach(function(alert) {
        dismissAlert(alert);
      });
    }

    // Helper function to dismiss a single alert
    function dismissAlert(alert) {
      if (alert && !alert.classList.contains('hiding')) {
        const closeButton = new bootstrap.Alert(alert);
        closeButton.close();
      }
    }
    
    // function to clear signup form
    function clearSignupForm() {
      document.getElementById("signupName").value = "";
      document.getElementById("signupEmail").value = "";
      document.getElementById("signupPassword").value = "";
      document.getElementById("confirmPassword").value = "";
      // uncheck agree terms checkbox
      const agreeTerms = document.getElementById("agreeTerms");
      if (agreeTerms) {
        agreeTerms.checked = false;
      }
    }
    
    // function to clear forgot password form
    function clearForgotPasswordForm() {
      document.getElementById("forgotEmail").value = "";
      if (document.getElementById("verificationCode")) {
        document.getElementById("verificationCode").value = "";
      }
      if (document.getElementById("newPassword")) {
        document.getElementById("newPassword").value = "";
      }
      if (document.getElementById("confirmNewPassword")) {
        document.getElementById("confirmNewPassword").value = "";
      }
    }

    loginTab.addEventListener("click", function () {
      dismissAllAlerts(); // Dismiss alerts on tab change
      hideAllForms();
      document.getElementById("login-form").classList.add("show", "active");
      resetTabStatus();
      loginTab.classList.add("active");
      loginTab.setAttribute("aria-selected", "true");
    });

    signupTab.addEventListener("click", function () {
      dismissAllAlerts(); // Dismiss alerts on tab change
      hideAllForms();
      document
        .getElementById("signup-form")
        .classList.add("show", "active");
      resetTabStatus();
      signupTab.classList.add("active");
      signupTab.setAttribute("aria-selected", "true");
    });

    // Forgot password link click event
    forgotPasswordLink.addEventListener("click", function () {
      dismissAllAlerts(); // Dismiss alerts on switching to forgot password
      hideAllForms();
      document
        .getElementById("forgot-password-form")
        .classList.add("show", "active");
      resetTabStatus();
    });

    // Back to login link click event
    backToLogin.addEventListener("click", function () {
      dismissAllAlerts(); // Dismiss alerts on back to login
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