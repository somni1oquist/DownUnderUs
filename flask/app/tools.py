from flask import jsonify
from sqlalchemy import or_
import pytz


def convert_timezone(timestamp, zone):
    '''Convert timestamp to local timezone. Default timezone is `Australia/Perth`'''
    utc = timestamp.replace(tzinfo=pytz.utc)
    timezone = pytz.timezone(zone if zone else 'Australia/Perth')
    format = '%a %d %B %Y %H:%M:%S'
    return utc.astimezone(timezone).strftime(format)

def json_response(status:str, message:str, opts:dict=None):
    '''Return a JSON response with `status` and `message`, and optional `data`.'''
    response = {"status": status, "message": message}

    if opts is None:
        return jsonify(response)
    
    response.update(opts)

    return jsonify(response)

def search_posts(content:str=None, topics:list=None, sort_by:str='timestamp_desc', limit:int=None, offset:int=None):
    '''Search posts based on content, topics, and sort_by. Return a list of posts.'''
    from .models import Post
    query_filter = Post.query
    results = query_filter

    # filter by content(incl. body and title)
    if content:
        query_filter = query_filter.filter(
            or_(
                Post.body.ilike(f"%{content}%"),
                Post.title.ilike(f"%{content}%")
            )
        )

    # filter by topics
    if topics:
        if type(topics) is not list:
            topics = topics.split(',')
        query_filter = query_filter.filter(Post.topic.in_(topics))

    # sort the results by views / timestamp and descending / ascending
    
    if sort_by:
        sort_column = sort_by.split('_')[0]
        reversed = True if sort_by.split('_')[1] == 'desc' else False
        results = query_filter.order_by(getattr(Post, sort_column).desc()\
                                        if reversed else getattr(Post, sort_column).asc())
    else:
        results = query_filter.order_by(Post.timestamp.desc())

    if offset:
        results = results.offset(offset)
    if limit:
        results = results.limit(limit)
        
    # return the results
    posts = []
    for post in results.all():
        post_dict ={
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "topic": post.topic,
            "user_id": post.user_id,
            "views": post.views,
            "timestamp": post.real_timestamp,
            "username": post.user.username
        }
        posts.append(post_dict)

    return posts