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
            case Action.EDIT:
                editReply($target);
                break;
            case Action.DELETE:
                console.log('Delete');
                break;
            case Action.UPVOTE:
                console.log('Upvote');
                break;
            case Action.DOWNVOTE:
                console.log('Downvote');
                break;
        }
    });
    const editReply = ($target) => {
        
    }
})