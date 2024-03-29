$(() => {
    const Action = {
        EDIT: 'edit',
        DELETE: 'delete',
        REPLY: 'reply',
        UPVOTE: 'upvote',
        DOWNVOTE: 'downvote'
    }
    $('div[id^="reply"] a[class*="btn"]').click(function(e) {
        e.preventDefault();
        const action = $(this).data('action');
        const $target = $(this).closest('div[id^="reply"]');
        switch(action) {
            case Action.REPLY: // Reply to post 
                reply($target);
                break;
            case Action.EDIT:
                edit($target);
                break;
            case Action.DELETE:
                const url = $(this).attr('href');
                if (confirm('Are you sure you want to delete this reply?'))
                    del(url);
                break;
            case Action.UPVOTE:
                console.log('Upvote');
                break;
            case Action.DOWNVOTE:
                console.log('Downvote');
                break;
        }
    });

    /**
     * Reply to post
     * @param {*} $target reply box
     */
    const reply = ($target) => {
        body = $target.find('textarea').val();
        console.log(body);
    }

    /**
     * Edit
     * @param {*} $target container
     */
    const edit = ($target) => {
        body = $target.find('div[class="card-text"]')[0].innerHTML.trim();
        console.log(body);
    }

    /**
     * Delete
     * @param {*} url delete endpoint
     */
    const del = (url) => {
        $.ajax({
            type: 'DELETE',
            url: url,
            success: function(response) {
                console.log(response);
                window.location.reload();
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
})