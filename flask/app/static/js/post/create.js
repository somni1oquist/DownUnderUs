import { BsType } from "../enums.js";
import { getTopics, makeToast, initEditor, getEditorContent } from "../utils.js";
// for create post feature
// This script is used to generate the drawdown list of topic
$(document).ready(function () {
  //get topic list
  getTopics().then(topics => {
    const menu = document.getElementById('topic-list');
      topics.forEach(topic => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.classList.add('dropdown-item');
        a.textContent = topic;
        // add event listerner to set the selected topic
        a.addEventListener('click', function (event) {
          // prevent default action
          event.preventDefault();
          document.getElementById('topic').value = topic;
        });
        li.appendChild(a);
        menu.appendChild(li);
      });
  })
  .catch(error => {
    makeToast(`Failed to get topics: ${error.message}`, BsType.DANGER, false);
  });

  initEditor($('#body')[0])

  // Handle the form submission for creating a new post
  const form = document.getElementById('createModal').querySelector('form');
  form.onsubmit = function (event) {
    //prevent form submission
    event.preventDefault();

    // ajax post request
    const formData = new FormData(form);
    const body = getEditorContent($('#body')[0]);
    const tags = $(body)
      .find('a[rel*=noopener]')
      .filter((_, el) => el.innerText.trim().startsWith('#'))
      .map((_, el) => el.innerText.trim().substring(1))
      .get();
    formData.append('body', body);
    formData.append('tags', tags);
    
    $.ajax({
      type: 'POST',
      url: '/post/create',
      data: formData,
      contentType: false,
      processData: false,
      success: (res) => {
        // Make a toast
        makeToast(res.message, BsType.SUCCESS)
          .then(() => {
            // close modal
            document.querySelector('.btn-secondary[data-bs-dismiss="modal"]').click();
            // clear form
            form.reset();
            // clear form errors
            clearFormErrors();
            // Redirect to the post page
            window.location.href = `/post/${res.post_id}`
          });
      },
      error: (err) => {
        displayFormErrors(form, err.responseJSON?.errors);
        makeToast(`Create post failed: ${err.responseJSON?.message}`, BsType.DANGER, false);
      }
    });
  };
});
// display form errors function
function displayFormErrors(form, errors) {
  var errorDivs = document.querySelectorAll('.invalid-feedback');
  errorDivs.forEach(function (errorDiv) {
    errorDiv.style.display = 'none';
    errorDiv.innerHTML = '';
  });

  for (var key in errors) {
    if (errors.hasOwnProperty(key)) {
      var input = form.querySelector('input[name="' + key + '"]') || $(form).find(`div#body`)[0];
      if (input) {
        var errorDiv = $(input).siblings('.invalid-feedback')[0];
        if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
          errorDiv.style.display = 'block';
          errorDiv.innerHTML = errors[key].join(', ');
        } else {
          console.error('No sibling with class "invalid-feedback" found for input', input);
        }
      } else {
        console.error('No input element found with name', key);
      }
    }

  }
};

function clearFormErrors() {
  var errorDivs = document.querySelectorAll('.invalid-feedback');
  errorDivs.forEach(function (errorDiv) {
    errorDiv.style.display = 'none';
    errorDiv.innerHTML = '';
  });
}