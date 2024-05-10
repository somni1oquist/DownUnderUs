import { BsType } from './enums.js';
import { makeToast } from './utils.js';
// When the page is loaded
$(window).on('load', () => {
  // Initialise all tooltips
  const $tooltips = $('[data-bs-toggle="tooltip"]')
  const tooltipList = [...$tooltips].map(tooltip => new bootstrap.Tooltip(tooltip))
});

$(() => {
  // When the window is resized, check the search result box height and hide the more button if necessary
  $(window).resize(checkOverflow);

  checkAndShowTitle();
  // Initial check for overflow
  checkOverflow();
  // Show the topics modal if the user has not selected any topics
  const showTopics = $('#showTopicsModal').val();
  if (showTopics) {
    const topicModal = new bootstrap.Modal('#topicModal', {
      backdrop: 'static',
      keyboard: false
    });
    topicModal.show();
  }

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

  // Inject CSRF token into AJAX requests
  // From https://flask-wtf.readthedocs.io/en/0.15.x/csrf/#javascript-requests
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      const csrfToken = $('#csrfToken').val();
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrfToken);
      }
    }
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

const checkOverflow = () => {
  // If the search result container does not exist, return
  if (!$('#search-result-container').length)
    return;

  const $seachResults = $('.search-post-body');
  const $more = $('.more');
  $seachResults.each((index, box) => {
    // Calculate the sum of the heights of all the children except the last one
    const height = [...box.children].slice(0, -1).reduce((acc, child) => acc + child.clientHeight, 0);
    if (height > box.clientHeight) {
      $more.eq(index).removeClass('d-none'); // Show "more" link
    } else {
      $more.eq(index).addClass('d-none'); // Hide "more" link
    }
  });
}