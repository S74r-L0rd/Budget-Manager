// Add f
// rgot password and return to login functionality
document.addEventListener("DOMContentLoaded", function () {
    // Handle tab switching for login and signup
    const loginTab = document.getElementById("login-tab");
    const signupTab = document.getElementById("signup-tab");
    const forgotPasswordLink = document.getElementById("forgotPasswordLink");
    const backToLogin = document.getElementById("backToLogin");
    
    // Get Code button for verification code
    const getCodeBtn = document.getElementById("getCodeBtn");
    const resetPasswordForm = document.getElementById("resetPasswordForm");
    
    const verifyCodeBtn = document.getElementById("verifyCodeBtn");
    const resetPasswordBtn = document.getElementById("resetPasswordBtn");
    
    // Get Code button click event
    if (getCodeBtn) {
      let timer;
      let countdown = 60;
      
      getCodeBtn.addEventListener("click", function() {
        const emailInputId = this.getAttribute("data-email");
        const emailInput = document.getElementById(emailInputId);
        
        if (!emailInput || !emailInput.value) {
          createAlert("please input your email address", "warning");
          return;
        }
        
        // Disable button immediately to prevent multiple clicks
        getCodeBtn.disabled = true;
        
        // Send AJAX request to get verification code
        const formData = new FormData();
        formData.append("email", emailInput.value);
        
        fetch("/get_verification_code", {
          method: "POST",
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === "success") {
            createAlert(data.message, "success");
            startCountdown();
          } else {
            createAlert(data.message, "danger");
            getCodeBtn.disabled = false;
          }
        })
        .catch(error => {
          console.error("Error:", error);
          createAlert("request failed, please try again later", "danger");
          getCodeBtn.disabled = false;
        });
      });
      
      // Function to start countdown
      function startCountdown() {
        countdown = 60;
        getCodeBtn.textContent = `${countdown}s`;
        
        timer = setInterval(function() {
          countdown--;
          getCodeBtn.textContent = `${countdown}s`;
          
          if (countdown <= 0) {
            clearInterval(timer);
            getCodeBtn.disabled = false;
            getCodeBtn.textContent = "Get Code";
          }
        }, 1000);
      }
    }

    // verify reset code button click event
    if (verifyCodeBtn) {
        verifyCodeBtn.onclick = function () {
            const email = document.getElementById("forgotEmail").value;
            const code = document.getElementById("verificationCode").value;
            if (!email || !code) {
                createAlert("please fill in email and verification code", "warning");
                return;
            }
            const formData = new FormData();
            formData.append("email", email);
            formData.append("code", code);

            fetch("/verify-reset-code", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    document.getElementById("passwordFields").style.display = "block";
                    verifyCodeBtn.style.display = "none";
                    resetPasswordBtn.style.display = "block";
                    createAlert(data.message, "success");
                } else {
                    createAlert(data.message, "danger");
                }
            })
            .catch(error => {
                createAlert("request failed, please try again later", "danger");
            });
        };
    }

    // handle reset password form submission
    if (resetPasswordForm) {
        resetPasswordForm.onsubmit = function (e) {
            e.preventDefault();
            const email = document.getElementById("forgotEmail").value;
            const newPassword = document.getElementById("newPassword").value;
            const confirmNewPassword = document.getElementById("confirmNewPassword").value;
            if (!newPassword || !confirmNewPassword) {
                createAlert("please fill in new password", "warning");
                return;
            }
            const formData = new FormData();
            formData.append("email", email);
            formData.append("new_password", newPassword);
            formData.append("confirm_password", confirmNewPassword);

            fetch("/reset-password", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    createAlert(data.message, "success");
                    setTimeout(() => {
                        window.location.href = "/login";
                    }, 2000);
                } else {
                    createAlert(data.message, "danger");
                }
            })
            .catch(error => {
                createAlert("request failed, please try again later", "danger");
            });
        };
    }

    // Function to create a dynamic alert
    function createAlert(message, type) {
      const alertContainer = document.getElementById("flash-messages");
      
      if (!alertContainer) return;
      
      const alertDiv = document.createElement("div");
      alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
      alertDiv.role = "alert";
      alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      `;
      
      alertContainer.appendChild(alertDiv);
      
      setTimeout(function() {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
      }, 5000);
    }

    // get all flash messages
    const flashMessages = document.querySelectorAll('.alert');
    
    // check if there is a clear form mark
    let shouldClearSignupForm = false;
    let shouldClearForgotForm = false;
    let shouldClearCodeField = false;
    let shouldClearPasswordFields = false;
    
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
        } else if (message === 'clear_code_field') {
          shouldClearCodeField = true;
          // hide this special message
          dismissAlert(alert);
        } else if (message === 'clear_password_fields') {
          shouldClearPasswordFields = true;
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
      // ensure forgot password form is active without clearing alerts
      if (!document.getElementById("forgot-password-form").classList.contains('active')) {
        showForgotPasswordFormWithoutDismissingAlerts();
      }
    }
    
    // if need to clear verification code field only
    if (shouldClearCodeField) {
      clearVerificationCodeField();
      // ensure forgot password form is active without clearing alerts
      if (!document.getElementById("forgot-password-form").classList.contains('active')) {
        showForgotPasswordFormWithoutDismissingAlerts();
      }
    }
    
    // if need to clear password fields only
    if (shouldClearPasswordFields) {
      clearPasswordFields();
      // ensure forgot password form is active without clearing alerts
      if (!document.getElementById("forgot-password-form").classList.contains('active')) {
        showForgotPasswordFormWithoutDismissingAlerts();
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
    
    // function to clear verification code field only
    function clearVerificationCodeField() {
      if (document.getElementById("verificationCode")) {
        document.getElementById("verificationCode").value = "";
      }
    }
    
    // function to clear password fields only
    function clearPasswordFields() {
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

    // show forgot password form without dismissing alerts
    function showForgotPasswordFormWithoutDismissingAlerts() {
      hideAllForms();
      document
        .getElementById("forgot-password-form")
        .classList.add("show", "active");
      resetTabStatus();
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

// Handle Terms and Privacy Modal
document.addEventListener('DOMContentLoaded', function() {
    const termsLinks = document.querySelectorAll('a[href="#"]');
    const termsModal = new bootstrap.Modal(document.getElementById('termsModal'));
    const termsContent = document.getElementById('termsContent');
    const privacyContent = document.getElementById('privacyContent');

    termsLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const isTerms = this.textContent.includes('Terms');
            
            // Show appropriate content
            termsContent.style.display = isTerms ? 'block' : 'none';
            privacyContent.style.display = isTerms ? 'none' : 'block';
            
            // Update modal title
            document.getElementById('termsModalLabel').textContent = 
                isTerms ? 'Terms of Service' : 'Privacy Policy';
            
            // Show modal
            termsModal.show();
        });
    });
});