// this script is used to generate posts and filter
document.addEventListener("DOMContentLoaded", function(showlist) {
  fetch('/post/topics') //get the list of topics
    .then(response => response.json())
    .then(data => {
      const topicBar = document.getElementById('topicBar');
      data.forEach(topic => {
        const topicItem = document.createElement('a');
        topicItem.href = "#";
        topicItem.classList.add('list-group-item', 'list-group-item-action');

        topicItem.textContent = topic;
        topicItem.onclick = function() { loadPostsByTopic(topic); };
        topicBar.appendChild(topicItem);
      });
    });
  //loads the display the list of posts in given topic
  function loadPostsByTopic(topic) {
    fetch(`/post/topics/${topic}`)
      .then(response => response.json())
      .then(posts => {
        const postList = document.getElementById('postList');
        //empty the existing posts
        postList.innerHTML = '';
        posts.forEach(post => {
          const postItem = document.createElement('div');
          postItem.innerHTML =`<details><summary><a href="/post/${post.id}">${post.title}</a></summary><pre>${post.body}</pre></details><small style="color: grey;">by ${post.username}——${post.timestamp}</small><hr>`;
          postList.appendChild(postItem);
        });
      });
  }
});
// When the page is loaded
$(window).on('load', () => {
  // Initialise all tooltips
  const $tooltips = $('[data-bs-toggle="tooltip"]')
  const tooltipList = [...$tooltips].map(tooltip => new bootstrap.Tooltip(tooltip))
});
/**
 * Handles sign-in by validating inputs and 
 * performing an AJAX request for server authentication.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Click event for sign-in button
    document.getElementById('signInButton').addEventListener('click', function(e) {
        e.preventDefault(); 

        // Retrieves user input
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorMessageDiv = document.getElementById('error-message');

        errorMessageDiv.style.display = 'none';
        
        // Check if either field is empty
        if (!username || !password) {
            errorMessageDiv.innerText = 'Please enter username and password.';
            errorMessageDiv.style.display = 'block';
        } else {
            // AJAX request for sign-in
            fetch('/auth/signin', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: username, password: password}),
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    throw new Error(data.message);
                }
                window.location.href = data.redirect;
            })
            .catch(error => {
                // Handles fetch errors
                console.error('Error:', error);
                errorMessageDiv.innerText = error.message;
                errorMessageDiv.style.display = 'block';
            });
        }
    });
});
