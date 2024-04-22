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
  const emojiList = ['😀', '😁', '😂', '😍'];
  const $dropdown = $('<div class="emoji-dropdown d-none">');
  // Create toolbar template
  emojiList.forEach(emoji => {
    $dropdown.append(`<span class="emoji">${emoji}</span>`);
  });
  $container.append($button.clone().addClass("ql-hashtag").append('<i class="fa-solid fa-hashtag">'))
  $container.append($button.clone().addClass("ql-emoji").append('<i class="fa-solid fa-face-smile">'))
  $container.append($dropdown)
  $container.append($button.clone().addClass("ql-img").append('<i class="fa-solid fa-image">'))
  $toolbar.append($container)
  $(target).before($toolbar)

  let selection = null; // Store the current selection for emoji insertion
  const editor = new Quill(target, {
    theme: 'snow',
    modules: {
      toolbar: {
        container: $toolbar[0],
        handlers: {
          'hashtag': () => {
            let tag = prompt('Enter the content of the hashtag:');
            if (tag) {
              tag = "#" + tag.replace(/ /g, "_");
              const range = editor.getSelection();
              if (range) {
                editor.insertText(range.index, " " + tag);
                editor.setSelection(range.index + tag.length + 1);
              }
            }
          },
          'emoji': () => {
            selection = editor.getSelection();
            $(editor.root).parent().siblings('.toolbar').find('.emoji-dropdown').toggleClass('d-none');
            $('.emoji').unbind('click'); // Remove any existing click event listeners
            $('.emoji').bind('click', (e) => {
              const emoji = $(e.target).text();
              const editor = $(e.target).closest('.toolbar').siblings('.ql-container').data('quill');
              if (selection) {
                // Insert the emoji at the current cursor position
                editor.insertText(selection.index, emoji);
                editor.setSelection(selection.index + emoji.length);
              }
              // Hide the dropdown after selecting an emoji
              $('.emoji-dropdown').addClass('d-none');
            });
          },
          'img': () => {
            // Create a hidden file input element
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*'; // Restrict to images only
            
            // When a file is selected, handle the file
            fileInput.onchange = async function(e) {
              const file = e.target.files[0];
              if (file) {
                const formData = new FormData();
                formData.append('image', file);

                try {
                  const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData,
                  });

                  if (response.ok) {
                    const data = await response.json();
                    const imageUrl = data.url;

                    const range = editor.getSelection();
                    editor.insertEmbed(range.index, 'image', imageUrl);
                    editor.setSelection(range.index + 1);
                  } else {
                    makeToast('Upload failed', BsType.DANGER, false);
                  }
                } catch (error) {
                  makeToast('Error uploading image', BsType.DANGER, false);
                }
              }
            };
            
            // Trigger the file input click to open the file selection dialog
            fileInput.click();
          }
        }
      }
    }
  });

  
  // Save the editor instance in the target element's data
  $(target).data('quill', editor);
  
  return editor;
};

/**
 * Get the content of the Quill editor
 * @param {string} container container element
 * @returns {string} content of the editor
 */
const getEditorContent = (container) => {
  const quill = $(container).data('quill');
  const content = quill.getSemanticHTML(0, quill.getLength());
  return content;
};

export { makeToast, getTopics, initEditor, getEditorContent }