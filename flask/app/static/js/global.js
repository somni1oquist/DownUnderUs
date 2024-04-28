import { BsType } from './enums.js';
import { makeToast } from './utils.js';
// When the page is loaded
$(window).on('load', () => {
  // Initialise all tooltips
  const $tooltips = $('[data-bs-toggle="tooltip"]')
  const tooltipList = [...$tooltips].map(tooltip => new bootstrap.Tooltip(tooltip))
});

$(() => {
  // When the create button is clicked
  $('a#create').on('click', (e) => {
    const $createModal = $('#createModal');
    // If the modal does not exist, redirect to sign-in page
    if (!$createModal.length) {
      e.preventDefault();
      makeToast(`Redirecting to sign-in page...`, BsType.PRIMARY)
        .then(() => window.location.href = '/auth/signin');
    }
  });
});

$(document).ready(function() {
  function checkAndShowTitle() {
      $.ajax({
          url: 'http://127.0.0.1:5000/profile/check-and-award-title', 
          type: 'GET', 
          success: function(response) {
            if (response.titles_awarded && response.titles_awarded.length > 0) {
                var titles = response.titles_awarded.join(", ");
                $('#titleAwardModal .modal-body').text('Congratulations! You have been awarded with: ' + titles);
            } else {
                $('#titleAwardModal .modal-body').text(response.message || 'No new titles were awarded.');
            }
            // Show the modal
            $('#titleAwardModal').modal('show'); 
        },
        
          error: function() {
              $('#titleAwardModal .modal-body').text('Failed to check titles.');
              $('#titleAwardModal').modal('show');
          }
      });
  }

  // Trigger this function when needed:
  checkAndShowTitle(); 
});