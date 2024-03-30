import { Action } from '../enum.js';
import { editPost, abortEdit, del, reply, editReply, save, vote } from './function.js';
$(() => {
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
        const title = $('#title-box').text();
        const body = $target.find('div[contenteditable="true"]').text();
        save(url, { title: title, body: body });
        break;

      case Action.ABORT:
        abortEdit($target);
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
        const body = $target.find('div[contenteditable="true"]').text();
        save(url, { body: body });
        break;

      case Action.ABORT:
        abortEdit($target);
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