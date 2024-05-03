from flask import jsonify
from sqlalchemy import or_,func
import pytz




def convert_timezone(timestamp, from_zone=None, to_zone='Australia/Perth', as_string=True):
    '''Convert timestamp between specified time zones.'''
    if from_zone is None:
        from_zone = 'UTC' 
    from_timezone = pytz.timezone(from_zone)
    to_timezone = pytz.timezone(to_zone)

    localized_timestamp = from_timezone.localize(timestamp)
    
    target_time = localized_timestamp.astimezone(to_timezone)
    
    if as_string:
        format = '%a %d %B %Y %H:%M:%S'
        return target_time.strftime(format)
    return target_time

def json_response(status:str, message:str, opts:dict=None):
    '''Return a JSON response with `status` and `message`, and optional `data`.'''
    response = {"status": status, "message": message}

    if opts is None:
        return jsonify(response) 
    
    response.update(opts)

    return jsonify(response)

def search_posts(content:str=None, topics:list=None, tags:str=None, \
                 sort_by:str='timestamp_desc', offset:int=None,\
                 page=1, per_page:int=10):
    '''Search posts based on content, topics, tags, and sort_by. Return a list of posts.
     Default limit is 10 posts per page.    
    '''
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

    '''
    error_out: bool, optional
     If set to True (the default), it causes the method to throw a 404 error if the page is out of range. 
     If set to False, it will instead return an empty list for out-of-range pages.
    '''
    pagination = results.paginate(page, per_page, error_out= False)
        
    return results,pagination

# set the user level based on the number of points
def user_level(user_id:int):
    from app.models import User
    #Return the user level based on the number of points.
    user = User.query.get(user_id)
    if user:
        if user.points < 201:
            return 'LV1'
        elif user.points < 401:
            return 'LV2'
        elif user.points < 601:
            return 'LV3'
        elif user.points < 801:
            return 'LV4'
        elif user.points < 1001:
            return 'LV5'
        else:
            return 'LV6'
    return 'Unknown Level'

