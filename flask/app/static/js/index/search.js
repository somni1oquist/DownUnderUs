import { getTopics } from "../utils.js";

$(() => {
	getTopics().then((topics) => {
		const $filterMenu = $('ul#filter-menu');
		topics.forEach((topic) => {
			const input = $('<input>').addClass('form-check-input')
				.attr('type', 'checkbox')
				.attr('role', 'switch')
				.attr('name', 'topics')
				.attr('value', topic)
				.attr('checked', 'checked');
			const label = $('<label>').addClass('form-check-label').attr('for', topic).text(topic);
			const switchDiv = $('<div>').addClass('form-check form-switch');
			switchDiv.append(input);
			switchDiv.append(label);
			const listItem = $('<li>').addClass('dropdown-item');
			listItem.append(switchDiv);
			$filterMenu.append(listItem);
		});
	});
});
