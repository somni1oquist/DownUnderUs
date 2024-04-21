import { makeToast } from "../utils.js";
import { BsType } from "../enums.js";

// Initialize the sign-in and sign-up after DOM content has loaded
document.addEventListener("DOMContentLoaded", function () {
  setupSignIn();
  setupSignUp();
});

/**
 * Adds an event listener to sign-in button
 * to handle user authentication via AJAX
 */
function setupSignIn() {
  const signInButton = document.getElementById("signInButton");
  if (signInButton) {
    signInButton.addEventListener("click", function (e) {
      e.preventDefault();
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const errorMessageDiv = document.getElementById("error-message");

      errorMessageDiv.style.display = "none";

      // Check if either field is empty
      if (!username || !password) {
        errorMessageDiv.innerText = "Please enter username and password";
        errorMessageDiv.style.display = "block";
      } else {
        // AJAX request for sign-in
        fetch("/auth/signin", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (!data.success) {
              throw new Error(data.message);
            }
            makeToast("Sign-in successful!", BsType.SUCCESS).then(
              () => (window.location.href = data.redirect)
            );
          })
          .catch((error) => {
            console.error("Error:", error);
            errorMessageDiv.innerText = error.message;
            errorMessageDiv.style.display = "block";
          });
      }
    });
  }
}

/**
 * Adds an event listener to sign-up button
 * to handle user registration via AJAX
 */
function setupSignUp() {
  const signUpButton = document.getElementById("signUpButton");
  if (signUpButton) {
    signUpButton.addEventListener("click", function (e) {
      e.preventDefault();
      const username = document.getElementById("username").value;
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      const confirmPassword = document.getElementById("confirm-password").value;
      const suburb = document.getElementById("suburb").value;
      const errorMessageDiv = document.getElementById("error-message");

      errorMessageDiv.style.display = "none";
      let errorMessage = "";

      // Validate inputs
      if (!username) {
        errorMessage = "Username is required";
      } else if (!email) {
        errorMessage = "Email is required";
      } else if (!password) {
        errorMessage = "Password is required";
      } else if (!confirmPassword) {
        errorMessage = "Confirm password is required";
      } else if (password !== confirmPassword) {
        errorMessage = "Passwords do not match";
      } else if (!suburb) {
        errorMessage = "Suburb is required";
      }

      if (errorMessage) {
        errorMessageDiv.innerText = errorMessage;
        errorMessageDiv.style.display = "block";
      } else {
        // Proceed with AJAX request
        fetch("/auth/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, email, password, suburb }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (!data.success) {
              throw new Error(data.message);
            }
            makeToast("Sign-up successful!", BsType.SUCCESS).then(
              () => (window.location.href = data.redirect)
            );
          })
          .catch((error) => {
            errorMessageDiv.innerText = error.message;
            errorMessageDiv.style.display = "block";
          });
      }
    });
  }
}
