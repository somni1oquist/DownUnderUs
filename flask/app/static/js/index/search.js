let changed = false;
$(() => {
	let timer;
	const $mobileSearchBody = $('div.mobile-search .search-body');
	const $searchBody = $('div.search-bar .search-body');
	// Reset input by params
	resetInputByParams();

	// Event listener for sort by
	$('input[name=sort-by]').on('change', function (e) {
		search(); // Search when sort by is changed
	});

	// Search input
	$('.search-body').on('keyup', function (e) {
		const isMobile = $(this).closest('.mobile-search').length > 0;

		// Synchronise the search input
		if (isMobile)
			$searchBody.val($(this).val());
		else
			$mobileSearchBody.val($(this).val());
		
		clearTimeout(timer);
		// Set timeout to prevent multiple requests
		timer = setTimeout(() => {
			search();
		}, 1000);
	});

	// Search button
	$('.search-button').on('click', function (e) {
		search();
	});

	// Event listener for topic filter
	$('#topics-container .dropdown-item').on('click', (e) => {
		addBadge($(e.currentTarget).text(), $('#topic-filter'));
	})
	// Firing serach when dropdown is hidden
	$('#topics-container .dropdown').on('hidden.bs.dropdown', (e) => {
		changed && search();
		changed = false; // Reset changed
	});
	// Remove topic
	$('#topic-filter, #tag-filter').on('click', 'span.badge', (e) => {
		$(e.currentTarget).remove();
		search();
	});

	// Event listener for hashtag
	$('#tags-container').on('click', 'button', (e) => {
		const tags = prompt('Enter tags separated by comma');
		if (tags) {
			const tagsArray = tags.split(',');
			tagsArray.forEach(tag => addBadge(tag.trim(), $('#tag-filter')));
			search();
		}
	});

	if (window.location.href.includes('search')) {
		$('#next-page a, #prev-page a').on('click', (e) => {
			e.preventDefault();
			const page = $(e.currentTarget).data('page');
			search(page);
		});
	}
});

/**
 * Add badge to filter
 * @param {string} content - Content of the badge
 * @param {JQuery<HTMLElement>} $filter - Filter to append the badge
 * @param {boolean} isReset - Flag to check if source is `resetInputByParams`
 */
const addBadge = (content, $filter, isReset = false) => {
	const template = `<span class="badge text-bg-secondary">${content}<i class="fa-solid fa-xmark"></i></span>`
	// Check if topic is already added
	const existing = $filter.find('span.badge').map(function () {
		return $(this).text();
	}).get().includes(content);
	if (existing) {
		return;
	}
	$filter.append(template);
	$filter.parent().removeClass('d-none');
	!isReset && (changed = true);
}

/**
 * Set params from input when searching
 * @returns {URLSearchParams} - URLSearchParams object
 */
const setParams = () => {
	const params = new URLSearchParams(window.location.search);
	const query = $('.search-body').val();
	// This can be undefined if nothing is selected
	const sortBy = $('input[name=sort-by]:checked').val();
	const topics = $('#topic-filter').find('span.badge').map(function () {
		return $(this).text();
	}).get();
	const tags = $('#tag-filter').find('span.badge').map(function () {
		return $(this).text();
	}).get();
	const isMobile = window.getComputedStyle($('.mobile-search')[0]).display !== 'none'

	// If mobile, sort by timestamp_desc
	if (isMobile) {
		params.set('query', query);
		params.set('sortBy', 'timestamp_desc');
		return params;
	}

	params.set('query', query);
	sortBy ? params.set('sortBy', sortBy) : params.delete('sortBy');
	params.set('topics', topics.join(','));
	params.set('tags', tags.join(','));

	return params;
};

/**
 * Reset input by params
 */
const resetInputByParams = () => {
	const params = new URLSearchParams(window.location.search);
	const query = params.get('query');
	const sortBy = params.get('sortBy');
	const topics = params.get('topics') ? params.get('topics').split(',') : [];
	const tags = params.get('tags') ? params.get('tags').split(',') : [];
	let sortLabel = 'New to Old';
	// Set input by params
	$('.search-body').val(query);

	if (sortBy) {
		$('input[name=sort-by]').each(function () {
			$(this).prop('checked', $(this).val() === sortBy);
		});
		sortLabel = $('input[name=sort-by]:checked').next().text();
	}
	$('#sort').text(sortLabel);

	topics.forEach(topic => { addBadge(topic, $('#topic-filter'), true) });
	tags.forEach(tag => { addBadge(tag, $('#tag-filter'), true) });
};

/**
 * Search
 */
const search = (page) => {
	const params = setParams();
	if (page)
		params.set('page', page);
	else
		params.delete('page');
	window.location.href = '/search?' + params.toString()
};