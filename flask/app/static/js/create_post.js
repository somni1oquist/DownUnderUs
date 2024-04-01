// for create post feature
// This script is used to generate the drawdown list of topic
$(document).ready(function () {
  //get topic list
  $.ajax({
    type: 'GET',
    url: '/post/topics',
    success: (res) => {
      const menu = document.getElementById('topic-list');
      const topics = res;
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
    },
    error: (err) => {
      // TODO: Use toast to show error message
      console.log('Failed to get topic list');
    }
  });

});


// This script is used to handle the form submission for creating a new post
$(document).ready(function () {
  const form = document.getElementById('exampleModal').querySelector('form');
  form.onsubmit = function (event) {
    //prevent form submission
    event.preventDefault();

    // ajax post request
    const formData = new FormData(form);
    $.ajax({
      type: 'POST',
      url: '/post/create-post',
      data: formData,
      contentType: false,
      processData: false,
      success: (res) => {
          // close modal
          // TODO: Use toast to show success message
          alert(res.message);
          document.querySelector('.btn-secondary[data-bs-dismiss="modal"]').click();
          // clear form
          form.reset();
          // clear form errors
          clearFormErrors();
          // Redirect to the post page
          window.location.href = `/post/${res.post_id}`
      },
      error: (err) => {
        displayFormErrors(res.errors);
        alert('Request failed');
      }
    });
  };

  // display form errors function
  function displayFormErrors(errors) {
    var errorDivs = document.querySelectorAll('.invalid-feedback');
    errorDivs.forEach(function (errorDiv) {
      errorDiv.style.display = 'none';
      errorDiv.innerHTML = '';
    });

    for (var key in errors) {
      if (errors.hasOwnProperty(key)) {
        var input = form.querySelector('input[name="' + key + '"], textarea[name="' + key + '"]');
        if (input) {
          var errorDiv = input.nextElementSibling;
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
});