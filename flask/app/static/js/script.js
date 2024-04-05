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
