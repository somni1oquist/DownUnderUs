import { BsType } from '../enums.js';
import { makeToast, getEditorContent, initEditor } from '../utils.js';
/**
 * Edit post
 * @param {*} $target container
 */
const editPost = ($target) => {
  const title = $('#title')[0].innerHTML.trim();
  const body = $target.find('div[class="card-text"]')[0].innerHTML.trim();

  const $original = $target.find('div[class="card-text"]');
  const $titleEditor = $('<h5 contenteditable="true" id="title-box"></h5>').text(title);
  const $contentEditor = $('<div id="editor" class="card-text"></div>').html(body);

  // Hide original text and edit button
  $original.addClass('d-none');
  $target.find('.btn[data-action="edit"]').addClass('d-none');

  // Reveal save and cancel buttons and append editor
  $target.find('.btn[data-action="save"], .btn[data-action="abort"]').removeClass('d-none');
  $target.find('div[class="card-body"]').append($titleEditor);
  $target.find('div[class="card-body"]').append($contentEditor);

  initEditor($contentEditor[0]);
  $contentEditor.focus();
};

/**
 * Reply to post
 * @param {*} $target reply box
 * @param {*} url reply endpoint
 */
const reply = ($target, url) => {
  const $container = $target.find('#reply-editor').length ? $target.find('#reply-editor') : $target.find('#modal-editor');
  const body = getEditorContent($container[0]);
  const tags = $(body)
    .find('a[rel*=noopener]')
    .filter((_, el) => el.innerText.trim().startsWith('#'))
    .map((_, el) => el.innerText.trim().substring(1))
    .get();
  const data = {
    body: body,
    tags: tags
  };
  create(url, data);
}
/**
 * Accept reply
 * @param {*} url accept endpoint
 */
const acceptReply = (url) => {
  $.ajax({
    type: 'PUT',
    url: url,
    contentType: 'application/json',
    success: (res) => {
      const message = res.message;
      makeToast(message, BsType.SUCCESS)
        .then(() => window.location.reload());
    },
    error: (err) => {
      const message = err.responseJSON.message;
      makeToast(`Accept failed: ${message}`, BsType.DANGER);
    }
  });
};

/**
 * Edit reply
 * @param {*} $target container
 */
const editReply = ($target) => {
  const body = $target.find('div[class="card-text"]')[0].innerHTML.trim();

  const $original = $target.find('div[class="card-text"]');
  const $editor = $('<div id="editor" class="card-text"></div>').html(body);

  // Hide original text and edit button
  $original.addClass('d-none');
  $target.find('.btn[data-action="edit"]').addClass('d-none');

  // Reveal save and cancel buttons and append editor
  $target.find('.btn[data-action="save"], .btn[data-action="abort"]').removeClass('d-none');
  $target.find('div[class="card-body"]').append($editor);
  initEditor($editor[0]);
  $editor.focus();
}

/**
 * Abort edit
 * @param {*} $target container
 */
const abortEdit = ($target) => {
  const $original = $target.find('div[class*="card-text"]:not([contenteditable="true"])');
  const $editor = $target.find('div#editor');
  // Show original text and edit button
  $original.removeClass('d-none');
  $target.find('.btn[data-action="edit"]').removeClass('d-none');
  // Hide save and cancel buttons and remove editor
  $editor.siblings('.toolbar').remove();
  $editor.siblings('#title-box').remove();
  $editor.remove();
  $target.find('.btn[data-action="save"], .btn[data-action="abort"]').addClass('d-none');
  makeToast('Edit aborted', BsType.WARNING, false);
}

/**
 * Save
 * @param {*} url edit endpoint
 * @param {*} data edited data
 */
const save = (url, data) => {
  // Extract tags from the body
  const tags = $(data.body)
    .find('a[rel*=noopener]')
    .filter((_, el) => el.innerText.trim().startsWith('#'))
    .map((_, el) => el.innerText.trim().substring(1))
    .get();
    data.tags = tags;

  $.ajax({
    type: 'PUT',
    url: url,
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: (res) => {
      const message = res.message;
      makeToast(message, BsType.SUCCESS)
        .then(() => window.location.reload());
    },
    error: (err) => {
      const message = err.responseJSON.message;
      makeToast(`Edit failed: ${message}`, BsType.DANGER, false);
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
      const message = res.message;
      makeToast(message, BsType.SUCCESS)
        .then(() => window.location.reload());
    },
    error: (err) => {
      const message = err.responseJSON.message;
      makeToast(`Reply failed: ${message}`, BsType.DANGER, false);
    }
  });
}

/**
 * Vote
 * @param {*} url vote endpoint
 */
const vote = (url) => {
  $.ajax({
    type: 'POST',
    url: url,
    contentType: 'application/json',
    data: JSON.stringify({
      vote: 'upvote'
    }),
    success: (res) => {
      const message = res.message;
      makeToast(message, BsType.SUCCESS)
        .then(() => window.location.reload());
    },
    error: (err) => {
      const message = err.responseJSON.message;
      makeToast(`Vote failed: ${message}`, BsType.DANGER, false);
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
      const message = res.message;
      const redirect = res.redirect;
      makeToast(message, BsType.SUCCESS)
        .then(() => {
          // Delete post
          if (redirect)
            window.location.href = redirect;
          // Delete reply
          else
            window.location.reload();
        });
    },
    error: (err) => {
      const message = err.responseJSON.message;
      makeToast(`Delete failed: ${message}`, BsType.DANGER, false);
    }
  });
}

export { editPost, reply, acceptReply, editReply, abortEdit, save, create, vote, del };