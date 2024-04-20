import { getTopics } from "../utils.js";

let changed = false; // Flag to check if input is changed
$(() => {
	let timer;
	const $filterMenu = $('ul#filter-menu');
	// Get topics
	getTopics().then((topics) => {
		// Add topics to filter menu
		topics.forEach((topic) => {
			const input = $('<input>').addClass('form-check-input')
				.attr('type', 'checkbox')
				.attr('role', 'switch')
				.attr('name', 'topics')
				.attr('value', topic)
				.attr('id', topic);
			const label = $('<label>').addClass('form-check-label').attr('for', topic).text(topic);
			const switchDiv = $('<div>').addClass('form-check form-switch form-switch-lg');
			switchDiv.append(input);
			switchDiv.append(label);
			const listItem = $('<li>').addClass('dropdown-item');
			listItem.append(switchDiv);
			$filterMenu.append(listItem);
		});

		// Reset input by params
		resetInputByParams();

		// Event listener for topics
		$('input[name=topics]').on('change', function (e) {
			changed = true;
		});
		// Event listener for sort by
		$('input[name=sort-by]').on('change', function (e) {
			search(); // Search when sort by is changed
		});
	});

	// Observe dropdowns for changes
	observe($('#search-filter')[0]);
	observe($('#search-sort')[0]);

	// Search input
	$('#search-body').on('keyup', function (e) {
		clearTimeout(timer);
		// Set timeout to prevent multiple requests
		timer = setTimeout(() => {
			search();
		}, 1000);
	});

	// Search button
	$('#search-button').on('click', function (e) {
		search();
	});

});

const observe = (target) => {
	const observer = new MutationObserver((mutationList, observer) => {
		for (let mutation of mutationList) {
			// Check if the dropdown is changed
			if (mutation.type === 'attributes' && mutation.attributeName === 'aria-expanded') {
				// Check if the dropdown is closed and selection changed
				if (mutation.target.getAttribute('aria-expanded') === 'false' && changed) {
					search();
					changed = false; // Reset status
				}
			}
		}
	})
	const opts = {
		attributes: true, // Listen for attribute changes
		attributeFilter: ['aria-expanded'] // Specify the attribute to observe
	};
	observer.observe(target, opts);
};

const setParams = () => {
	const params = new URLSearchParams(window.location.search);
	const query = $('#search-body').val();
	const topics = $('input[name=topics]:checked').map(function () {
		return $(this).val();
	}).get();
	const sortBy = $('input[name=sort-by]:checked').val();

	params.set('query', query);
	params.set('topics', topics);
	params.set('sortBy', sortBy);

	return params;
};

const resetInputByParams = () => {
	const params = new URLSearchParams(window.location.search);
	const query = params.get('query');
	const topics = params.get('topics') ? params.get('topics').split(',') : [];
	const sortBy = params.get('sortBy');

	// Set input by params
	$('#search-body').val(query);

	if (topics.length) {
		$('input[name=topics]').each(function () {
			topics.includes($(this).val()) ? $(this).attr('checked', true) : $(this).removeAttr('checked');
		});
	} else {
		$('input[name=topics]').each(function () {
			$(this).attr('checked', true);
		});
	}

	if (sortBy) {
		$('input[name=sort-by]').each(function () {
			$(this).prop('checked', $(this).val() === sortBy);
		});
	}
};

const search = () => {
	const params = setParams();
	window.location.href = '/search?' + params.toString()
};
