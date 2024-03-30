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
      // TODO: Use toast or moal before reload
      window.location.reload();
    },
    error: (err) => {
      // TODO: Use toast instead of alert or console.log
      console.log(err);
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
      // TODO: Use toast or moal before reload
      window.location.reload();
    },
    error: (err) => {
      // TODO: Use toast instead of alert or console.log
      console.log(err);
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
      // TODO: Use toast before reload
      window.location.reload();
    },
    error: (err) => {
      // TODO: Use toast instead of alert
      // Vote already cast
      alert(err.responseJSON.message);
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
      // TODO: Use toast or modal before reload
      window.location.reload();
    },
    error: (err) => {
      // TODO: Use toast instead of alert or consolg.log
      console.log(err);
    }
  });
}

export { editPost, reply, editReply, abortEdit, save, create, vote, del };