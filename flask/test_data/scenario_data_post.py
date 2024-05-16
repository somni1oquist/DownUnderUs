from faker import Faker
import random
from app import db
from app.models import Post, Reply
from datetime import datetime, timedelta

fake = Faker()

# All users' pswd is 'test123'
def create_post(content, post_date, title, location, topic, selected_tags, img_path, user_id, last_edited=None):
    timestamp = datetime.strptime(post_date, "%Y-%m-%d %H:%M:%S")
    views = random.randint(0, 1000)
    if last_edited is None:
        last_edited = timestamp + timedelta(hours=random.randint(0, 100))
    votes = random.randint(0, 500)

    # Convert newlines to <br> for HTML
    formatted_content = content.replace("\n", "<br>")
    
    # Add tags as hyperlinks
    if selected_tags:
        hash_tag = ' '.join([f'<a href="#" rel="noopener noreferrer">{tag}</a>' for tag in selected_tags])
        body = f'{hash_tag}<br><p>{formatted_content}</p>'
    else:
        body = f'<p>{formatted_content}</p>'
    
    # Add images
    if img_path:
        img =  f'<img src="{img_path}" alt="Uploaded Image">'
        body = f'{body}<br>{img}'

    tags = ','.join(selected_tags)

    post = Post(
        title=title,
        body=body,
        views=views,
        votes=votes,
        user_id=user_id,
        topic=topic,
        tags=tags,
        location=location,
        timestamp=timestamp,
        last_edited=last_edited
    )
    db.session.add(post)
    db.session.commit()
    return post.id

def create_replies(content, reply_date, post_id=None, img_path=None, accepted=False, parent_id=None, user_id=None, votes=None, last_edited=None):
    if votes is None:
        votes = random.randint(0, 100)
    delta_hours = random.randint(0, 100)
    timestamp = datetime.strptime(reply_date, "%Y-%m-%d %H:%M:%S")
    if last_edited is None:
        # last_edited time must be greater than timestamp
        last_edited = timestamp + timedelta(hours=delta_hours)
    if user_id is None:
        user_id = random.randint(1, 20)  # Assuming we have 20 users

    # Convert newlines to <br> for HTML
    formatted_content = content.replace("\n", "<br>")
    
    # Construct the reply body
    body = f'<p>{formatted_content}</p>'
    
    # Add images
    if img_path:
        img = f'<img src="{img_path}" alt="Uploaded Image">'
        body = f'{body}<br>{img}'
    
    reply = Reply(
        body=body,
        votes=votes,
        timestamp=timestamp,
        last_edited=last_edited,
        user_id=user_id,
        post_id=post_id,
        accepted=accepted,
        parent_id=parent_id
    )
    db.session.add(reply)
    db.session.commit()
    return reply.id
