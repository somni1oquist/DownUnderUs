import { BsType } from './enums.js';
/**
 * Make a toast
 * @param {*} message message to be displayed
 * @param {*} type type of toast e.g. success, danger, warning, info
 * @param {*} freeze freeze the page to prevent interaction from users, by default true
 * @param {*} duration milliseconds to show the toast by default 2000ms
 */
const makeToast = (message, type, freeze, duration) => {
  const typeClass = `text-bg-${type}`;
  // Disable user interaction with the page
  const $mask = $('div.lmask');
  const toFreeze = freeze === undefined ? true : freeze;
  toFreeze && $mask.show(); // Show the mask if freeze is true

  switch (type) {
    case BsType.SUCCESS:
      message = `<i class="fa-solid fa-circle-check"></i> ${message}`;
      break;
    case BsType.DANGER:
      message = `<i class="fa-solid fa-circle-exclamation"></i> ${message}`;
      break;
    case BsType.WARNING:
      message = `<i class="fa-solid fa-triangle-exclamation"></i> ${message}`;
      break;
    case BsType.INFO:
      message = `<i class="fa-solid fa-circle-info"></i> ${message}`;
      break;
  }

  return new Promise((resolve, reject) => {
    const $actionToast = $('div#action-toast');
    $actionToast.find('div.toast-body').html(message);
    $actionToast.addClass(typeClass);
    const toast = new bootstrap.Toast($actionToast[0], {
      autohide: true,
      delay: duration || 2000 // 2 seconds
    });

    const handleHidden = () => {
      $actionToast.removeClass(typeClass);
      $actionToast.off('hidden.bs.toast', handleHidden); // Remove the event listener
      // Allow the user to interact with the page again
      toFreeze && $mask.hide();

      resolve(); // Resolve the Promise when the toast is hidden
    };

    $actionToast.on('hidden.bs.toast', handleHidden);
    toast.show();
  });
};

export { makeToast }