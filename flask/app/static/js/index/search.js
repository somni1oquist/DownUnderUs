import { getTopics } from "../utils.js";

// auto submit the search form when the user selects a filter or sort option
document.addEventListener('DOMContentLoaded', function () {

	const filterSelect = document.getElementById('search-filter');
	const sortSelect = document.getElementById('search-sort');


	if (filterSelect) {
		getTopics().then(topics => {
			// create a default option
			const defaultOption = document.createElement('option');
			defaultOption.value = '';
			defaultOption.textContent = 'All Topics';
			filterSelect.appendChild(defaultOption);
			topics.forEach(topic => {
				const option = document.createElement('option');
				option.value = topic;
				option.textContent = topic;
				filterSelect.appendChild(option);
			});
		});
		
		filterSelect.addEventListener('change', function () {
			this.form.submit();
		});
	}

	if (sortSelect) {
		sortSelect.addEventListener('change', function () {
			this.form.submit();
		});
	}
	
	
})
