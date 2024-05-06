import { BsType } from './enums.js';
import { makeToast } from './utils.js';
// When the page is loaded
$(window).on('load', () => {
  // Initialise all tooltips
  const $tooltips = $('[data-bs-toggle="tooltip"]')
  const tooltipList = [...$tooltips].map(tooltip => new bootstrap.Tooltip(tooltip))
});

$(() => {
  checkAndShowTitle();
  
  // When the create button is clicked
  $('a#create').on('click', (e) => {
    const $createModal = $('#createModal');
    // If the modal does not exist, redirect to sign-in page
    if (!$createModal.length) {
      e.preventDefault();
      makeToast(`Redirecting to sign-in page...`, BsType.PRIMARY, true, 2000, 'top-center', 'md')
        .then(() => window.location.href = '/auth/signin');
    }
  });

  // When a tag in page body is clicked
  $('a[rel*=noopener]').on('click', (e) => {
    e.preventDefault();
    const tag = $(e.currentTarget).text()?.split('#')[1];
    // Redirect to the search page with the tag as the search query
    window.location.href = `/search?tags=${tag}`;
  });

  // close bottom banner
  $('.banner-header .btn-close').on('click', (e) => {
    $(e.target).closest('.bottom-banner').hide();
});

});

const checkAndShowTitle = () => {
  $.ajax({
      url: '/profile/check-and-award-title', 
      type: 'GET', 
      success: function(response) {
        if (response?.titles_awarded && response.titles_awarded.length > 0) {
            var titles = response.titles_awarded.join(", ");
            makeToast('Congratulations! You have been awarded with: ' + titles, BsType.SUCCESS, true, 5000, 'top-center', 'md')
        } 
    },
    error: function(error) {
        console.log(error);
    }
  });
}


