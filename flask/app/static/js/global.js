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