import { makeToast } from '../utils.js';
import { BsType } from '../enums.js';
$(() => {
  let init = true;
  // Check if the user has selected at least 2 topics and at most 6 topics
  $('#topicModal .form-check input').on('click', function(e) {
    checkSelections(this, init);
    init = false;
  });

  // Submit the form when the user clicks the 'Next' button
  $('#topicModal #next').on('click', function() {
    const selected_topics = $('.form-check input[aria-pressed=true]').map((_, el) => el.value).get();
    if (selected_topics.length >= 2 && selected_topics.length <= 6) {
      const url = $(this).closest('.modal-content').find('form').attr('action')
      const showTopics = $('#showTopicsModal').val();
      const callbackUrl = !showTopics ? '/profile' : undefined;
      const data = { topics: selected_topics, callbackUrl: callbackUrl };
      $.ajax({
        url: url,
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(response) {
          makeToast(response.message, BsType.SUCCESS)
            .then(() => window.location.href = response.redirect);
        },
        error: function(err) {
          makeToast(err.responseJSON.message, BsType.DANGER, false);
        }
      });
    }
  });
})
const checkSelections = (target, init) => {
  const selectedTopics = $('.form-check input[aria-pressed=true]').map((_, el) => el.value).get();
  if (selectedTopics.length < 2 && !init) {
    makeToast('You must select at least 2 topics', BsType.WARNING, false);
    $(target).attr('aria-pressed', true).addClass('active');
  } else if (selectedTopics.length > 6) {
    $(target).attr('aria-pressed', false).removeClass('active');
    makeToast('You can only select up to 6 topics', BsType.WARNING, false);
  }
}