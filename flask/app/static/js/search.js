import { BsType } from "./enums.js";
import { makeToast } from "./utils.js";

// this script is used to generate search results
document.getElementById('search-form').addEventListener('submit', function (event) {
	event.preventDefault();
	const query = document.getElementById('search-input').value;
	const sortBy = document.getElementById('search-sort').value;
	const topic = document.getElementById('search-filter').value;

	// encodeURIComponent is used to encode special characters in the query
	$.ajax({
		url: `/post/search?q=${encodeURIComponent(query)}&sort=${encodeURIComponent(sortBy)}&topic=${encodeURIComponent(topic)}`,
		type: 'GET',
		dataType: 'json',
		success: function (data) {
			const searchResults = document.getElementById('search-result-container');
			// clear the search results
			searchResults.innerHTML = '';
			if (!data.length) {
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
												<span><i class="fa-solid fa-feather"></i> ${post.timestamp}</span>
												<span>
													<i class="fa-solid fa-eye"></i> ${post.views}
												</span>
											</div>
										</div>
								`;
					searchResults.appendChild(resultBox);
				})
			}
		},
		error: function (error) {
			makeToast(`Search error: ${error.responseJSON.message}`, BsType.WARNING, false);
		}
	});
});

// this script is used to validate the search input
document.getElementById('search-input').addEventListener('input', function () {
	const inputValue = this.value;
	if (inputValue.length > 0 && inputValue.length < 3) {
		document.getElementById('input-error').style.display = 'flex';
	} else {
		document.getElementById('input-error').style.display = 'none';
	}
});


document.addEventListener('DOMContentLoaded', function () {

	fetch('/post/topics')
			.then(response => response.json()) 
			.then(topics => {
					const menu = document.getElementById('search-filter');
					// create a default option
					const defaultOption = document.createElement('option');
					defaultOption.value = ''; 
					defaultOption.textContent = 'All Topics'; 
					menu.appendChild(defaultOption);
					topics.forEach(topic => {
							const option = document.createElement('option');
							option.value = topic; 
							option.textContent = topic; 
							menu.appendChild(option);
					});
			})
			.catch(error => console.error('Error fetching topic list', error));
});
