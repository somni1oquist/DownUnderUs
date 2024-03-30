import { BsType } from '../enum.js';

/**
 * Make a toast
 * @param {*} message message to be displayed
 * @param {*} type type of toast e.g. success, danger, warning, info
 */
const makeToast = (message, type) => {
  const typeClass = `text-bg-${type}`;

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
      delay: 2000 // 2 seconds
    });

    const handleHidden = () => {
      $actionToast.removeClass(typeClass);
      $actionToast.off('hidden.bs.toast', handleHidden); // Remove the event listener
      resolve(); // Resolve the Promise when the toast is hidden
    };

    $actionToast.on('hidden.bs.toast', handleHidden);
    toast.show();
  });
};

/**
 * Edit post
 * @param {*} $target container
 */
const editPost = ($target) => {
  const title = $('#title')[0].innerHTML.trim();
  const body = $target.find('div[class="card-text"]')[0].innerHTML.trim();

  const $original = $target.find('div[class="card-text"]');
  const $titleEditor = $('<h5 contenteditable="true" id="title-box"></h5>').text(title);
  const $contentEditor = $('<div contenteditable="true" class="card-text"></div>').html(body);

  // Hide original text and edit button
  $original.addClass('d-none');
  $target.find('.btn[data-action="edit"]').addClass('d-none');

  // Reveal save and cancel buttons and append editor
  $target.find('.btn[data-action="save"], .btn[data-action="abort"]').removeClass('d-none');
  $target.find('div[class="card-body"]').append($titleEditor);
  $target.find('div[class="card-body"]').append($contentEditor);

  $contentEditor.focus();
};

/**
 * Reply to post
 * @param {*} $target reply box
 * @param {*} url reply endpoint
 */
const reply = ($target, url) => {
  const body = $target.find('textarea').val();
  const data = {
    body: body
  };
  create(url, data);
}

/**
 * Edit reply
 * @param {*} $target container
 */
const editReply = ($target) => {
  const body = $target.find('div[class="card-text"]')[0].innerHTML.trim();

  const $original = $target.find('div[class="card-text"]');
  // TODO: Integrate WYSIWYG editor instead of pure text
  const $editor = $('<div contenteditable="true" class="card-text"></div>').text(body);

  // Hide original text and edit button
  $original.addClass('d-none');
  $target.find('.btn[data-action="edit"]').addClass('d-none');

  // Reveal save and cancel buttons and append editor
  $target.find('.btn[data-action="save"], .btn[data-action="abort"]').removeClass('d-none');
  $target.find('div[class="card-body"]').append($editor);
  $editor.focus();
}

/**
 * Abort edit
 * @param {*} $target container
 */
const abortEdit = ($target) => {
  const $original = $target.find('div[class*="card-text"]:not([contenteditable="true"])');
  const $editor = $target.find('[contenteditable="true"]');
  // Show original text and edit button
  $original.removeClass('d-none');
  $target.find('.btn[data-action="edit"]').removeClass('d-none');
  // Hide save and cancel buttons and remove editor
  $editor.remove();
  $target.find('.btn[data-action="save"], .btn[data-action="abort"]').addClass('d-none');
  makeToast('Edit aborted', BsType.WARNING);
}

/**
 * Save
 * @param {*} url edit endpoint
 * @param {*} data edited data
 */
const save = (url, data) => {
  $.ajax({
    type: 'PUT',
    url: url,
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: (res) => {
      makeToast('Edit saved', BsType.SUCCESS)
        .then(() => window.location.reload());
    },
    error: (err) => {
      const message = err.responseJSON.message;
      makeToast(`Edit failed: ${message}`, BsType.DANGER);
    }
  });
}

/**
 * Create
 * @param {*} url create endpoint
 * @param {*} data data to be sent
 */
const create = (url, data) => {
  $.ajax({
    type: 'POST',
    url: url,
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: (res) => {
      makeToast('Reply posted', BsType.SUCCESS)
        .then(() => window.location.reload());
    },
    error: (err) => {
      const message = err.responseJSON.message;
      makeToast(`Reply failed: ${message}`, BsType.DANGER);
    }
  });
}

/**
 * Vote
 * @param {*} url vote endpoint
 * @param {*} action upvote or downvote
 */
const vote = (url, action) => {
  $.ajax({
    type: 'PUT',
    url: url,
    contentType: 'application/json',
    data: JSON.stringify({
      vote: action
    }),
    success: (res) => {
      makeToast('Vote cast', BsType.SUCCESS)
        .then(() => window.location.reload());
    },
    error: (err) => {
      const message = err.responseJSON.message;
      makeToast(`Vote failed: ${message}`, BsType.DANGER);
    }
  });
}

/**
 * Delete
 * @param {*} url delete endpoint
 */
const del = (url) => {
  $.ajax({
    type: 'DELETE',
    url: url,
    success: (res) => {
      makeToast('Post deleted', BsType.SUCCESS)
        .then(() => window.location.reload());
    },
    error: (err) => {
      const message = err.responseJSON.message;
      makeToast(`Delete failed: ${message}`, BsType.DANGER);
    }
  });
}

export { editPost, reply, editReply, abortEdit, save, create, vote, del };