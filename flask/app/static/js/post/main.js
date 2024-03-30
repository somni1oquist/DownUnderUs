import { Action } from '../enum.js';
import { del, reply, editReply, save, vote } from './function.js';
$(() => {
  // Event listener for post actions
  $('div[id="post"] a[class*="btn"]').click(function (e) {
    e.preventDefault(); // Prevent default action
    const action = $(this).data('action');
    const url = $(this).attr('href');
    const $target = $(this).closest('div[id="post"]');

    switch (action) {
      case Action.EDIT:
        console.log('Edit post');
        break;

      case Action.SAVE:
        console.log('Save post');
        break;

      case Action.ABORT:
        console.log('Abort edit');
        break;

      case Action.DELETE:
        if (confirm('Are you sure you want to delete this post?'))
          del(url);
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
      case Action.REPLY: // Reply to post 
        reply($target, url);
        break;

      case Action.EDIT:
        editReply($target, url);
        break;

      case Action.SAVE:
        const body = $target.find('div[class="card-text"]').text();
        save(url, { body: body });
        break;

      case Action.ABORT:
        const $original = $target.find('div[class*="card-text"]:not([contenteditable="true"])');
        const $editor = $target.find('div[class="card-text"][contenteditable="true"]');
        // Show original text and edit button
        $original.removeClass('d-none');
        $target.find('.btn[data-action="edit"]').removeClass('d-none');
        // Hide save and cancel buttons and remove editor
        $editor.remove();
        $target.find('.btn[data-action="save"], .btn[data-action="abort"]').addClass('d-none');
        break;

      case Action.DELETE:
        if (confirm('Are you sure you want to delete this reply?'))
          del(url);
        break;

      case Action.UPVOTE:
      case Action.DOWNVOTE:
        vote(url, action);
        break;
    }
  });
})