
// When the page is loaded
$(window).on('load', () => {
  // Initialise all tooltips
  const $tooltips = $('[data-bs-toggle="tooltip"]')
  const tooltipList = [...$tooltips].map(tooltip => new bootstrap.Tooltip(tooltip))
});

