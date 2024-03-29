$(() => {
    const Action = {
        EDIT: 'edit',
        DELETE: 'delete',
        REPLY: 'reply',
        UPVOTE: 'upvote',
        DOWNVOTE: 'downvote'
    };
    $('div[id^="reply"] a[class*="btn"]').click(function(e) {
        e.preventDefault();
        const action = $(this).data('action');
        const url = $(this).attr('href');
        const $target = $(this).closest('div[id^="reply"]');
        switch(action) {
            case Action.REPLY: // Reply to post 
                reply($target, url);
                break;
            case Action.EDIT:
                edit($target, url);
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
        body = $target.find('textarea').val();
        data = {
            body: body
        };
        create(url, data);
    }

    /**
     * Edit reply
     * @param {*} $target container
     */
    const edit = ($target) => {
        body = $target.find('div[class="card-text"]')[0].innerHTML.trim();
        console.log(body);
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
                window.location.reload();
            },
            error: (err) => {
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
                window.location.reload();
            },
            error: (err) => {
                console.log(err);
            }
        });
    }
})