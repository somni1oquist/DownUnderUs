from flask import jsonify
from sqlalchemy import or_,func
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

def search_posts(content:str=None, topics:list=None, tags:str=None, sort_by:str='timestamp_desc', limit:int=None, offset:int=None):
    '''Search posts based on content, topics, tags, and sort_by. Return a list of posts.'''
    from .models import Post,User
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

    # filter by tags
    if tags:
        query_filter = query_filter.filter(Post.tags.ilike(f"%{tags}%"))


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
            "username": post.user.username,
            "tags": post.tags,
            "level": user_level(post.user_id)
        }
       
        posts.append(post_dict)
    
    return posts

def user_level(user_id:int):
    from app.models import User
    #Return the user level based on the number of points.
    user = User.query.get(user_id)
    if user:
        if user.points < 201:
            return 'Level 1'
        elif user.points < 401:
            return 'Level 2'
        elif user.points < 601:
            return 'Level 3'
        elif user.points < 801:
            return 'Level 4'
        elif user.points < 1001:
            return 'Level 5'
        else:
            return 'Level 6'
    return 'Unknown Level'

