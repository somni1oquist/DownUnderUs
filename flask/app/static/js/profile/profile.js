import { makeToast } from '../utils.js';
import { BsType } from '../enums.js';

document.addEventListener("DOMContentLoaded", function () {
  // Add event listener to all elements with data-action attribute
  $('a[data-action], button[data-action]').on('click', function (e) {
    e.preventDefault();
    const action = $(this).data('action');
    const oldVal = $(this).prev()?.text(); // Get the old value in the previous element
    const url = $(this).attr('href') || $(this).data('url');

    // Switch case to handle different actions
    switch (action) {
      case 'upload-image':
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.accept = "image/*";
        fileInput.style.display = "none";
        fileInput.onchange = function () {
          if (fileInput.files.length > 0)
            uploadProfileImage(url, fileInput.files[0]);
        }
        document.body.appendChild(fileInput);
        fileInput.click();
        document.body.removeChild(fileInput);
        break;
      case 'delete-image':
        const confirmDelete = confirm('Are you sure you want to delete your profile image?');
        if (!confirmDelete) return;
        deleteProfileImage(url);
        break;
      case 'edit-topics':
        const topicModal = new bootstrap.Modal('#topicModal', {
          backdrop: 'static',
          keyboard: false
        });
        topicModal.show();
        break;
      case 'edit-username':
        const username = prompt('Enter new username:', oldVal);
        if (username === null || username === oldVal) return;
        // Send a post request to update user's profile
        editProfile({username: username}, url, () => {
          // Set the new value to the previous element
          $(this).prev().text(username);
        });
        break;
      case 'edit-email':
        const email = prompt('Enter new email:', oldVal);
        if (email === null || email === oldVal) return;
        // Send a post request to update user's profile
        editProfile({email: email}, url, () => {
          // Set the new value to the previous element
          $(this).prev().text(email);
        });
        break;
      case 'edit-suburb':
        $(this).addClass('d-none'); // Hide the edit button
        $(this).siblings('span').addClass('d-none'); // Hide the old value
        $(this).siblings('select').removeClass('d-none'); // Show the input field
        $(this).siblings('a[data-action]').removeClass('d-none'); // Show the save and abort button
        // Send a post request to update user's profile
        break;
      case 'save-suburb':
        const suburb = $(this).siblings('select').val(); // Get the new value from the input field
        // Send a post request to update user's profile
        editProfile({suburb: suburb}, url, () => {
          $(this).siblings('span').text(suburb).removeClass('d-none'); // Set the new value to the previous element
          $(this).addClass('d-none').next().addClass('d-none'); // Hide the save and abort button
          $(this).siblings('select').addClass('d-none'); // Hide the input field
          $(this).siblings('a[data-action=edit-suburb]').removeClass('d-none'); // Hide the edit and abort button
        });
        break;
      case 'abort-suburb':
        $(this).addClass('d-none').prev().addClass('d-none'); // Hide the abort and save button
        $(this).siblings('select').addClass('d-none'); // Hide the input field
        $(this).siblings('a[data-action=edit-suburb]').removeClass('d-none'); // Show the edit button
        $(this).siblings('span').removeClass('d-none'); // Show the old value
        break;
      case 'change-password':
        changePassword(url, () => {
          $('#changePasswordModal').modal('hide');
        })
        break;
    }
  });

});
/**
 * Send a post request to delete user's profile image
 * @param {string} url - The url to send the request to
 * @param {object} file - The file to send in the request
 */
const uploadProfileImage = (url, file) => {
  const formData = new FormData();
  formData.append("image", file);

  $.ajax({
    url: url,
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    success: function (response) {
      makeToast(response.message, BsType.SUCCESS, true, 1500)
        .then(() => {
          const imageUrl = response.url;
          const image = `<img id="profile-image" src="${imageUrl}" alt="Profile Image">`;
          $('#image-container').find('#profile-image').remove();
          $('#image-container').find('[data-action="delete-image"]').removeClass('d-none');
          $('#image-container').prepend(image);
        });
    },
    error: function (error) {
      makeToast(error.responseJSON?.message, BsType.DANGER, false);
    }
  });
}

/**
 * Send a delete request to delete user's profile image
 * @param {string} url - The url to send the request to
 */
const deleteProfileImage = (url) => {
  $.ajax({
    url: url,
    type: 'DELETE',
    success: function (response) {
      makeToast(response.message, BsType.SUCCESS, true, 1500)
        .then(() => {
          $('#image-container').find('img#profile-image').remove();
          $('#image-container').find('[data-action="delete-image"]').addClass('d-none');
          $('#image-container').prepend('<i id="profile-image" class="fa-solid fa-user-circle fa-10x"></i>');
        });
    },
    error: function (error) {
      makeToast(error.responseJSON?.message, BsType.DANGER, false);
    }
  });
}

/**
 * Send a post request to update user's profile
 * @param {object} data - The data to send in the request
 * @param {string} url - The url to send the request to
 * @param {function} callback - The function to call after the request is successful
 */
const editProfile = (data, url, callback) => {
  $.ajax({
    url: url,
    type: 'PUT',
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: function (response) {
      makeToast(response.message, BsType.SUCCESS, false, 1500)
        .then(() => { callback() });
    },
    error: function (error) {
      makeToast(error.responseJSON?.message, BsType.DANGER, false);
    }
  });
};

/**
 * Send a post request to change user's password
 * @param {string} url - The url to send the request to
 * @param {function} callback - The function to call after the request is successful
 */
const changePassword = (url, callback) => {
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

  const data = {
    currentPassword: currentPassword,
    newPassword: newPassword,
  };

  $.ajax({
    url: url,
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: function (response) {
      makeToast(response.message, BsType.SUCCESS, true, 2000, 'top-center')
        .then(() => { callback() });
    },
    error: function (error) {
      makeToast(error.responseJSON?.message, BsType.DANGER, false, 2000, 'top-center');
    }
  });
};