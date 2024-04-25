document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("submitChangePassword")
    .addEventListener("click", function () {
      changePassword();
    });

  $("#changePasswordModal").on("hidden.bs.modal", function () {
    document.getElementById("password-messages").style.display = "none";
  });

  document
    .getElementById("saveProfileButton")
    .addEventListener("click", function () {
      updateProfile();
    });

  document
    .getElementById("closeProfileButton")
    .addEventListener("click", function () {
      window.location.href = "/profile/";
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

  // Check if the password fields are filled
  if (!currentPassword) {
    messageDiv.style.display = "block";
    messageDiv.className = "alert alert-danger";
    messageDiv.textContent = "Please enter the current password.";
    return;
  }

  if (!newPassword || !confirmPassword) {
    messageDiv.style.display = "block";
    messageDiv.className = "alert alert-danger";
    messageDiv.textContent = "Please enter both new password fields.";
    return;
  }

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
      }
    })
    .catch((error) => {
      messageDiv.style.display = "block";
      messageDiv.className = "alert alert-danger";
      messageDiv.textContent = "Failed to update profile. Please try again.";
    });
}
