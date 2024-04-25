document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("uploadImageButton")
    .addEventListener("click", function () {
      const fileInput = document.createElement("input");
      fileInput.type = "file";
      fileInput.accept = "image/*";
      fileInput.style.display = "none";

      fileInput.onchange = function (e) {
        if (fileInput.files.length > 0) {
          uploadProfileImage(fileInput.files[0]);
        }
      };

      document.body.appendChild(fileInput);
      fileInput.click();
      document.body.removeChild(fileInput);
    });
});

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
        console.log("Image URL after upload", imageUrl);
        return fetch("/profile/update_image", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ imageUrl: imageUrl }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(
                "Failed to update profile image. Server responded with status: " +
                  response.status
              );
            }
            return response.json();
          })
          .then((updateData) => {
            if (updateData.status === "success") {
              document.getElementById("profileImage").src = imageUrl;
              displayMessage("Profile image updated successfully.", "success");
            } else {
              throw new Error(updateData.message);
            }
          });
      } else {
        throw new Error(data.message);
      }
    })
    .catch((error) => {
      displayMessage("Failed to upload image. " + error.message, "danger");
    });
}

function displayMessage(message, type) {
  const messageDiv = document.getElementById("form-messages");
  messageDiv.textContent = message;
  messageDiv.className = `alert alert-${type}`;
  messageDiv.style.display = "block";
  setTimeout(() => {
    messageDiv.style.display = "none";
  }, 5000);
}
