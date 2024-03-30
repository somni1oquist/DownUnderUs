$(() => {
    // Constants for actions
    const Action = {
        EDIT: 'edit',
        SAVE: 'save',
        ABORT: 'abort',
        DELETE: 'delete',
        REPLY: 'reply',
        UPVOTE: 'upvote',
        DOWNVOTE: 'downvote'
    };

    // Event listener for post actions
    $('div[id="post"] a[class*="btn"]').click(function(e) {
        e.preventDefault(); // Prevent default action
        const action = $(this).data('action');
        const url = $(this).attr('href');
        const $target = $(this).closest('div[id="post"]');

        switch(action) {
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
    $('div[id^="reply"] a[class*="btn"]').click(function(e) {
        e.preventDefault(); // Prevent default action
        const action = $(this).data('action');
        const url = $(this).attr('href');
        const $target = $(this).closest('div[id^="reply"]');

        switch(action) {
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
})