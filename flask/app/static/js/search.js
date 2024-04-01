// this script is used to generate search results
document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('search-input').value;
    const sortBy = document.getElementById('search-sort').value;
    const topic = document.getElementById('search-filter').value;

    // encodeURIComponent is used to encode special characters in the query
    fetch(`/post/search?q=${encodeURIComponent(query)}&sort=${encodeURIComponent(sortBy)}&topic=${encodeURIComponent(topic)}`)
    .then(response => response.json())
    .then(data=> {
        console.log(data);
        const searchResults = document.getElementById('search-result-container');
        // clear the search results
        searchResults.innerHTML = '';
        if (data.length === 0) {
            searchResults.innerHTML = '<p> No results found </p>';
        } else {
            data.forEach(post => {  

                const resultBox = document.createElement('div');
                resultBox.innerHTML = `
                    <div class="search-result-box">
                        <h4><a href="/post/${post.id}">${post.title}</a></h4>

                        <div class="search-author-info">
                            <img src="../../static/images/icons8-bmo-48.png" alt="author photo">
                            <span>${post.username}</span>

                        </div>

                        <div class="search-post-body">
                            <p>${post.body}</p>
                        </div>

                        <div class="search-footer">
                            <span>Published: ${post.timestamp}</span>
                            <span>
                            Views:${post.views}
                            </span>
                        </div>
                    </div>
                `;
                searchResults.appendChild(resultBox);
            })
        }
    })
    .catch(error => console.error('Error fetching search results:', error));

})

// this script is used to validate the search input
document.getElementById('search-input').addEventListener('input', function() {
    const inputValue = this.value;
    if (inputValue.length > 0 && inputValue.length < 3) {
        document.getElementById('input-error').style.display = 'flex';
    } else {
        document.getElementById('input-error').style.display = 'none';
    }
});

// This script is used to generate the drawdown filter list of topic
document.addEventListener('DOMContentLoaded', function() {
    //get topic list
    fetch('../../static/files/topic.txt')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n');
            const menu = document.getElementById('search-filter');
            lines.forEach(line => {
                const option = document.createElement('option');
                option.value = line.trim();
                option.textContent = line.trim();
                menu.appendChild(option);});
        })
        .catch(error => console.error('Error fetching topic list', error));
})