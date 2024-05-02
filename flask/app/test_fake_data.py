from faker import Faker
import random
from app import db
from app.models import Post, User, Title as tableTitle, Reply,Vote
from app.enums import Topic,Title as enumTitle
import datetime
import requests
import os
from flask import current_app as app

fake = Faker()
TAGS = [
    'urban', 'rural', 'education', 'public transport', 'infrastructure',
    'healthcare', 'sports', 'community', 'safety', 'technology',
    'environment', 'governance', 'culture', 'leisure', 'real estate'
]

suburbs = [
    "Perth", "Armadale", "Bayswater", "Canning", "Cockburn", "Fremantle",
    "Gosnells", "Joondalup", "Kalamunda", "Kwinana", "Melville"
]

def create_fake_posts(num_posts=50):
    for _ in range(num_posts):
        body = fake.text(max_nb_chars=400)
        timestamp = fake.date_time_this_year()
        user_id = random.randint(1, 20)  # Assuming we have 20 users
        title = fake.sentence(nb_words=6)
        views = random.randint(0, 1000)
        last_edited = timestamp + datetime.timedelta(hours=random.randint(0, 100))
        topic = random.choice(list(Topic)).value
        votes = random.randint(0, 500)
        location = random.choice(suburbs)
        tags = ', '.join(random.sample(TAGS, random.randint(2, 5)))
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


topic_values = [topic.value for topic in Topic]
def create_fake_users(num_users=20):
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password_hash = fake.password()
        suburb =random.choice(suburbs)
        interested_topics = ', '.join(random.sample(topic_values, random.randint(2, 6)))
        points = random.randint(0, 1000)
        registered_date = fake.date_time_this_year()
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            suburb=suburb,
            interested_topics=interested_topics,
            points=points,
            registered_date=registered_date
        )
        db.session.add(user)
    db.session.commit()


def create_fake_titles(num_titles=20):
    for user_id in range(1, 11):
        num_titles_for_user = random.randint(1, 6) # Each user can have 1-6 titles
        selected_titles = random.sample(list(enumTitle), num_titles_for_user)
        for title in selected_titles:
            awarded_date = fake.date_time_this_year()
            title_data = tableTitle(
                title=title.value,
                user_id=user_id,
                awarded_date=awarded_date
            )
            db.session.add(title_data)
        db.session.commit()

def create_fake_replies(num_reply=100):
    for _ in range(num_reply):
        body = fake.text(max_nb_chars=400)
        votes = random.randint(0, 100)
        timestamp = fake.date_time_this_year()
        delta_hours=random.randint(0, 100)
        # last_edited time must be greater than timestamp
        last_edited = timestamp + datetime.timedelta(hours=delta_hours)
        user_id = random.randint(1, 20) # Assuming we have 20 users
        post_id = random.randint(1, 50) # Assuming we have 50 posts
        accepted = random.choice([True, False])
        parent_id = random.choice([None, random.randint(1, 50)])
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

def create_fake_vote(num_vote = 50):
    for _ in range(num_vote):
        user_id = random.randint(1, 20) # Assuming we have 20 users
        reply_id = random.randint(1, 100) # Assuming we have 100 replies
        vote_type = "upvote"
        vote = Vote(
            user_id=user_id,
            reply_id=reply_id,
            vote_type=vote_type
        )
        db.session.add(vote)
    db.session.commit()

'''
>>> fake.image_url()
'https://picsum.photos/718/859'
'''

def download_image(img_url):
    response = requests.get(img_url)
    if response.status_code == 200:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        image_name = ".jpg"
        filename = os.urandom(16).hex() + image_name  
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # write the image to the file
        with open(file_path, 'wb') as file:
            file.write(response.content) 
        return filename  
    return None 

def update_profile_img(user_id, filename):
    user = User.query.get(user_id)
    if user:
        user.profile_image = filename
        db.session.commit()

def create_fake_profile_img(num_img=20):
    for i in range(1,num_img+1):
        # img 200*200
        img_url = fake.image_url(200,200)
        filename = download_image(img_url)
        if filename:
            user_id = i
            update_profile_img(user_id, filename)
            print(f"Updated user {user_id} with new image {filename}") 

def create_fake_data():
    create_fake_users()
    print("Created 20 fake users")
    create_fake_posts()
    print("Created 50 fake posts")
    create_fake_titles()
    print("Created 20 fake titles")
    create_fake_replies()
    print("Created 100 fake replies")
    create_fake_vote()
    print("Created 50 fake votes")
    create_fake_profile_img()
    print("Created 20 fake profile images")