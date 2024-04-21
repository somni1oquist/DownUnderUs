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

/**
 * Get topics from the server
 * @param {boolean} refresh whether to refresh the topics, by default false
 */
const getTopics = (refresh = false) => {
  return new Promise((resolve, reject) => {
    const topics = sessionStorage.getItem('topics');
    
    if (topics && !refresh) {
      // If topics are available in sessionStorage, resolve the Promise with them
      resolve(JSON.parse(topics));
    } else {
      const url = '/post/topics';
      $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
          const topics = response.topics;
          sessionStorage.setItem('topics', JSON.stringify(topics));
          // Resolve the Promise with the fetched topics
          resolve(topics);
        },
        error: function(err) {
          // If there's an error, reject the Promise with the error message
          reject(err.responseJSON.message);
        }
      });
    }
  });
};

/**
 * Initialize the Quill editor
 * @param {string} target target element to initialize the editor
 * @returns {Quill} Quill editor instance
 */
const initEditor = (target) => {
  const $toolbar = $('<div class="toolbar">');
  const $container = $('<span class="ql-formats">');
  const $button = $('<button type="button">')
  $container.append($button.clone().addClass("hashtag").append('<i class="fa-solid fa-hashtag">'))
  $container.append($button.clone().addClass("emoji").append('<i class="fa-solid fa-face-smile">'))
  $container.append($button.clone().addClass("image").append('<i class="fa-solid fa-image">'))
  $toolbar.append($container)
  $(target).before($toolbar)

  const editor = new Quill(target, {
    theme: 'snow',
    modules: {
      toolbar: $toolbar[0]
    }
  });
  // Save the editor instance in the target element's data
  $(target).data('quill', editor);
  
  return editor;
};

/**
 * Get the content of the Quill editor
 * @param {Quill} quill Quill editor instance
 * @returns {string} content of the editor
 */
const getEditorContent = (quill) => {
  const content = quill.getSemanticHTML(0, quill.getLength());
  return content;
};

export { makeToast, getTopics, initEditor, getEditorContent }