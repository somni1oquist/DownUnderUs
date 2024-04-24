document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("submitChangePassword")
    .addEventListener("click", function () {
      changePassword();
    });

  $("#changePasswordModal").on("hidden.bs.modal", function () {
    document.getElementById("password-messages").style.display = "none";
  });
});

let initialUserData = {
  username: document.getElementById("username").value,
  email: document.getElementById("email").value,
  suburb: document.getElementById("suburb").value,
};

/**
 * Send a post request to update user's profile
 */
function updateProfile() {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const suburb = document.getElementById("suburb").value;

  const updatedFields = [];
  if (username !== initialUserData.username) updatedFields.push("username");
  if (email !== initialUserData.email) updatedFields.push("email");
  if (suburb !== initialUserData.suburb) updatedFields.push("suburb");

  if (updatedFields.length === 0) {
    displayMessage("No changes to update.", "info");
    return;
  }

  const data = JSON.stringify({
    username: username,
    email: email,
    suburb: suburb,
  });

  fetch("/profile/edit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: data,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        initialUserData.username = username;
        initialUserData.email = email;
        initialUserData.suburb = suburb;

        displayMessage(
          `Updated ${updatedFields.join(", ")} successfully.`,
          "success"
        );
      } else {
        displayMessage(data.message, "danger");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      displayMessage("Failed to update profile. Please try again.", "danger");
    });
}

function displayMessage(message, type) {
  const messageDiv = document.getElementById("form-messages");
  messageDiv.textContent = message;
  messageDiv.className = `alert alert-${type}`;
  messageDiv.style.display = "block";

  // Hide the message after 5 seconds
  setTimeout(() => {
    messageDiv.style.display = "none";
  }, 5000);
}

/**
 * Validate and change user's password
 */
function changePassword() {
  const currentPassword = document.getElementById("current-password").value;
  const newPassword = document.getElementById("new-password").value;
  const confirmPassword = document.getElementById("confirm-new-password").value;
  const messageDiv = document.getElementById("password-messages");

  messageDiv.style.display = "none";

  // Check if current password is entered
  if (!currentPassword) {
    messageDiv.style.display = "block";
    messageDiv.className = "alert alert-danger";
    messageDiv.textContent = "Please enter the current password.";
    return;
  }

  // Proceed to verify current password
  verifyCurrentPassword(currentPassword)
    .then((isCorrect) => {
      if (!isCorrect) {
        messageDiv.style.display = "block";
        messageDiv.className = "alert alert-danger";
        messageDiv.textContent = "Incorrect current password.";
        return;
      }

      messageDiv.style.display = "none";

      // Check if new password fields are blank
      if (!newPassword || !confirmPassword) {
        messageDiv.style.display = "block";
        messageDiv.className = "alert alert-danger";
        messageDiv.textContent = "Please enter both new password fields.";
        return;
      }

      // If the new password fields are not blank, proceed with validation of new password
      if (newPassword !== confirmPassword) {
        messageDiv.style.display = "block";
        messageDiv.className = "alert alert-danger";
        messageDiv.textContent = "New passwords do not match.";
        return;
      }

      const data = JSON.stringify({
        currentPassword: currentPassword,
        newPassword: newPassword,
      });

      fetch("/profile/password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: data,
      })
        .then((response) => response.json())
        .then((data) => {
          messageDiv.style.display = "block";
          messageDiv.className = data.success
            ? "alert alert-success"
            : "alert alert-danger";
          messageDiv.textContent = data.message;

          // If password change was successful, reset the form fields
          if (data.success) {
            document.getElementById("current-password").value = "";
            document.getElementById("new-password").value = "";
            document.getElementById("confirm-new-password").value = "";
            currentPasswordCorrect = false;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    })
    .catch((error) => {
      console.error("Error verifying current password:", error);
    });
}

/**
 * Sends a request to verify the correctness of the current password.
 * @param {string} currentPassword - The current password input by the user.
 * @returns {Promise} - A promise that resolves to whether the password is correct.
 */
function verifyCurrentPassword(currentPassword) {
  return fetch("/profile/verify-password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ password: currentPassword }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      return data.isCorrect;
    })
    .catch((error) => {
      console.error("Error verifying current password:", error);
      throw error;
    });
}
