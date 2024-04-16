import { getTopics } from "../utils.js";

$(() => {
	const params = new URLSearchParams(window.location.search);
	let timer;
	getTopics().then((topics) => {
		const $filterMenu = $('ul#filter-menu');
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

		// Get search parameters
		getParams();

		// Set event listeners after topics are loaded
		$('input[name=topics], input[name=sort-by]').on('change', function (e) {
			search(params);
		});
	});
	// Search input
	$('#search-body').on('keyup', function (e) {
		clearTimeout(timer);
		timer = setTimeout(() => {
			search(params);
		}, 1000);
	});
	// Search button
	$('#search-button').on('click', function (e) {
		search(params);
	});
});

const setParams = (params) => {
	const query = $('#search-body').val();
	const topics = $('input[name=topics]:checked').map(function () {
		return $(this).val();
	}).get();
	const sortBy = $('input[name=sort-by]:checked').val();

	params.set('query', query);
	params.set('topics', topics);
	params.set('sortBy', sortBy);
};

const getParams = () => {
	const params = new URLSearchParams(window.location.search);
	const query = params.get('query');
	const topics = params.get('topics') ? params.get('topics').split(',') : [];
	const sortBy = params.get('sortBy');

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

const search = (params) => {
	setParams(params);
	window.location.href = '/search?' + params.toString()
};
