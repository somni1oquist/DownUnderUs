import { Action, BsType } from '../enums.js';
import { initEditor, getEditorContent, makeToast } from '../utils.js';
import { editPost, abortEdit, del, reply, acceptReply, editReply, save, vote } from './functions.js';
$(() => {
  // Initialise editor
  const $editor = $('#reply-editor');
  const $modalEditor = $('#replyModal #modal-editor');
  if ($editor.length)
    initEditor($editor[0], false);
  if ($modalEditor.length)
    initEditor($modalEditor[0], false);

  $('#title-btn').on('click', () => {
    const $title = $('#title');
    const title = prompt('Enter title', $title.text());
    const url = $('#title-btn').data('url');
    if (title.trim())
      save(url, { title: title });
  });

  // Event listener for location button
  $('#location').on('click', () => {
    const location = prompt('Enter location (leave empty to remove location)');
    const url = $('#location').data('url');
    if (location.trim()) {
      // Save location
      save(url, { location: location});
    } else if (location !== null || location.trim() === '') {
      // Remove location
      save(url, { location: "null" });
    }
  })

  // Event listener for post actions
  $('div[id="post"] a[class*="btn"]').click(function (e) {
    e.preventDefault(); // Prevent default action
    const action = $(this).data('action');
    const url = $(this).attr('href');
    const $target = $(this).closest('div[id="post"]');

    switch (action) {
      case Action.EDIT:
        editPost($target);
        break;

      case Action.SAVE:
        const $editor = $target.find('div#editor');
        const body = getEditorContent($editor[0]);
        // Extract tags from the body
        const tags = $(body)
          .find('a[rel*=noopener]')
          .filter((_, el) => el.innerText.trim().startsWith('#'))
          .map((_, el) => el.innerText.trim().substring(1))
          .get();
        // Empty post = <p></p>
        if ($(body).text().length === 0 && $(body).find('img').length === 0) {
          makeToast('Please reply with more contents', BsType.WARNING, false);
          return;
        }

        save(url, { body: body, tags: tags});
        break;

      case Action.ABORT:
        confirm('Are you sure you want to abort editing?') && abortEdit($target);
        break;

      case Action.DELETE:
        confirm('Are you sure you want to delete this post?') && del(url);
        break;
    }
  });

  // Even listener for reply actions
  $('div[id^="reply"] a[class*="btn"]').click(function (e) {
    e.preventDefault(); // Prevent default action
    const action = $(this).data('action');
    const url = $(this).attr('href');
    const $target = $(this).closest('div[id^="reply"]');

    switch (action) {
      case Action.MODAL:
        const $modal = $('#replyModal');
        const username = $(this).data('reply-username');
        // Set the modal title
        $modal.find('.modal-title').text(`Reply to ${username}`);
        // Set the url to the button
        $modal.find('button:not([data-bs-dismiss])').data('url', url);
        $modal.modal('show');
        break;

      case Action.REPLY: // Reply to post
        confirm('Are you sure to reply?') && reply($target, url);
        break;

      case Action.ACCEPT: // Accept reply
        confirm('Are you sure to accept this reply?') && acceptReply(url);
        break;

      case Action.EDIT:
        editReply($target, url);
        break;

      case Action.SAVE:
        const $editor = $target.find('div#editor');
        const body = getEditorContent($editor[0]);
        // Empty reply = <p></p>
        if ($(body).text().length === 0 && $(body).find('img').length === 0) {
          makeToast('Please reply with more contents', BsType.WARNING, false);
          return;
        }
        save(url, { body: body });
        break;

      case Action.ABORT:
        confirm('Are you sure to abort editing?') && abortEdit($target);
        break;

      case Action.DELETE:
        confirm('Are you sure to delete this reply?') && del(url);
        break;

      case Action.UPVOTE:
        vote(url);
        break;
    }
  });

  // Event listener for image
  $('.post-container .card-text img').on('click', function (e) {
    const src = $(this).attr('src');
    const $modal = $('#imageModal');
    $modal.find('img').attr('src', src);
    $modal.show();
  });
  // Event listener for image modal
  $('#imageModal').on('click', function (e) {
    $(this).hide().find('img').attr('src', '');
  });

  // Event listener for reply modal
  $('#replyModal #send-reply').on('click', function (e) {
    e.preventDefault(); // Prevent default action
    const url = $(this).data('url');
    const $target = $('#replyModal')
    reply($target, url);
  });
})