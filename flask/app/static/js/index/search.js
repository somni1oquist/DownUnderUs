import { BsType } from "../enums.js";
import { makeToast } from "../utils.js";


// auto submit the search form when the user selects a filter or sort option
document.addEventListener('DOMContentLoaded', function() {

	var filterSelect = document.getElementById('search-filter');
	var sortSelect = document.getElementById('search-sort');


	filterSelect.addEventListener('change', function() {
			this.form.submit();  
	});

	sortSelect.addEventListener('change', function() {
			this.form.submit();  
	});
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
})
