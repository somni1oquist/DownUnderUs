import { BsType } from "./enums.js";
import { makeToast } from "./utils.js";
// this script is used to generate posts and filter
document.addEventListener("DOMContentLoaded", function () {
  // Add event listener to the topic bar
  $('#topicBar').find('a').click(function (e) {
    e.preventDefault();
    loadPostsByTopic($(this).text().trim());
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
        postItem.innerHTML = `
          <details>
            <summary>
              <a href="/post/${post.id}">${post.title}</a>
            </summary>
            <pre>${post.body}</pre>
          </details>
          <small style="color: grey;">by ${post.username}——${post.timestamp}</small>
          <hr>`;
        postList.appendChild(postItem);
      });
    })
    .catch(error => {
      makeToast(`Error: ${error.message}`, BsType.DANGER)
    });
};