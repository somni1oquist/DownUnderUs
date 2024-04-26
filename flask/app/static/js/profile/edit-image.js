document.addEventListener("DOMContentLoaded", function () {
  bindDynamicButtons();
});

/**
 * Bind dynamic buttons to their respective event handlers
 */
function bindDynamicButtons() {
  const uploadButton = document.getElementById("uploadImageButton");
  if (uploadButton) {
    uploadButton.addEventListener("click", function () {
      const fileInput = document.createElement("input");
      fileInput.type = "file";
      fileInput.accept = "image/*";
      fileInput.style.display = "none";

      fileInput.onchange = function () {
        if (fileInput.files.length > 0) {
          uploadProfileImage(fileInput.files[0]);
        }
      };

      document.body.appendChild(fileInput);
      fileInput.click();
      document.body.removeChild(fileInput);
    });
  }

  const deleteButton = document.getElementById("deleteImageButton");
  if (deleteButton) {
    deleteButton.addEventListener("click", function () {
      deleteProfileImage();
    });
  }
}

/**
 * Uploads the profile image to the server
 * @param {*} file The file to be uploaded
 */
function uploadProfileImage(file) {
  const formData = new FormData();
  formData.append("image", file);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        const imageUrl = data.url;
        fetch("/profile/update_image", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ imageUrl: imageUrl }),
        })
          .then((response) => response.json())
          .then((updateData) => {
            if (updateData.status === "success") {
              setProfileImage(imageUrl);
              displayMessage("Profile image updated successfully.", "success");
            } else {
              throw new Error(updateData.message);
            }
          })
          .catch((error) => {
            displayMessage(
              "Failed to update profile image. " + error.message,
              "danger"
            );
          });
      } else {
        throw new Error(data.message);
      }
    })
    .catch((error) => {
      displayMessage("Failed to upload image. " + error.message, "danger");
    });
}

/**
 * Deletes the profile image from the server
 */
function deleteProfileImage() {
  fetch("/profile/delete_image", {
    method: "DELETE",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          "Failed to delete profile image. Server responded with status: " +
            response.status
        );
      }
      return response.json();
    })
    .then((data) => {
      if (data.status === "success") {
        removeProfileImage();
        displayMessage("Profile image deleted successfully.", "success");
      } else {
        throw new Error(data.message);
      }
    })
    .catch((error) => {
      displayMessage(
        "Failed to delete profile image. " + error.message,
        "danger"
      );
    });
}

/**
 * Sets the profile image in the UI
 * @param {*} imageUrl The URL of the profile image
 */
function setProfileImage(imageUrl) {
  const container = document.getElementById("profileImageContainer");
  container.innerHTML = `
    <img id="profileImage" src="${imageUrl}" alt="Profile Image" class="img-fluid profile-img rounded-circle">
    <button type="button" id="deleteImageButton" class="btn btn-primary mt-2">Delete Image</button>
    <button type="button" id="uploadImageButton" class="btn btn-primary mt-2">Upload Image</button>
  `;
  bindDynamicButtons();
}

function removeProfileImage() {
  const container = document.getElementById("profileImageContainer");
  container.innerHTML = `
    <i class="fas fa-user-circle fa-10x text-secondary my-large-icon"></i>
    <button type="button" id="uploadImageButton" class="btn btn-primary mt-2">Upload Image</button>
  `;
  bindDynamicButtons();
}

/**
 * Displays a message to the user.
 * @param {string} message The message to display.
 * @param {string} type The type of message (e.g., success, danger).
 */
function displayMessage(message, type) {
  const messageDiv = document.getElementById("form-messages");
  messageDiv.textContent = message;
  messageDiv.className = `alert alert-${type}`;
  messageDiv.style.display = "block";
  setTimeout(() => {
    messageDiv.style.display = "none";
  }, 5000);
}
