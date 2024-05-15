from faker import Faker
import random
from app import db
from app.models import Post, User, Title as tableTitle, Reply,Vote
from app.enums import Topic,Title as enumTitle
import datetime
import requests
import os
from flask import current_app as app
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from test_data.scenario1 import scenario1
from test_data.scenario2 import scenario2
from test_data.scenario3 import scenario3

fake = Faker()
topic_tags = {
"Rentals": ["apartment", "lease", "tenant", "landlord", "rent_agreement"],
    "Pets": ["dogs", "cats", "pet_care", "veterinarian", "pet_adoption"],
    "Gardening": ["plants", "horticulture", "landscaping", "gardening_tools", "flower_gardening"],
    "Give and Take": ["swap", "exchange", "freebies", "donation", "recycle"],
    "Job": ["career", "part-time_jobs", "interviews", "hiring", "resumes"],
    "Food and Cooking": ["recipes", "cooking_tips", "healthy_eating", "baking", "foodie"],
    "Sports and Games": ["fitness", "team_sports", "board_games", "outdoor_activities", "competitions"],
    "Ride Share": ["carpool", "commuting", "rides", "transportation", "eco-friendly_travel"],
    "Pick Up and Delivery": ["courier", "package", "mail", "delivery_services", "logistics"],
    "Social": ["events", "meetups", "community", "networking", "social_media"]
}

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
        votes = random.randint(0, 500)
        location = random.choice(suburbs)
        topic = random.choice(list(Topic)).value
        TAGS = topic_tags[topic]
        selected_tags = random.sample(TAGS, random.randint(2, 5))
        for tag in selected_tags:
            hash_tag = '<a href="#" rel="noopener noreferrer">#' + tag + '</a>'
            body = hash_tag + ' ' + body
        tags = ', '.join(selected_tags)
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
        password_hash = generate_password_hash('test123')
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

def create_fake_depth1_replies(num_reply=50):
    # use set to make sure we don't accept the same post twice
    accepted_replies=set()
    for _ in range(num_reply):
        body = fake.text(max_nb_chars=400)
        votes = random.randint(0, 100)
        user_id = random.randint(1, 20) # Assuming we have 20 users
        post_id = random.randint(1, 50) # Assuming we have 50 posts

        # reply timestamp must be greater than post timestamp
        delta_hours=random.randint(0, 100)
        parent_id = None
        post = Post.query.filter_by(id=post_id).first()
        timestamp = post.timestamp + datetime.timedelta(hours=delta_hours)
        # last_edited time must be greater than timestamp
        last_edited = timestamp + datetime.timedelta(hours=delta_hours)
        if post_id in accepted_replies:
            accepted = False
        else:
            accepted = random.choice([True, False])
            if accepted:
                accepted_replies.add(post_id)

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

# reply depth more than 2
def create_fake_depth2_replies(num_reply=50,parent_id=None):
    for _ in range(num_reply):
        body = fake.text(max_nb_chars=400)
        votes = random.randint(0, 100)
        user_id = random.randint(1, 20) # Assuming we have 20 users
        # reply timestamp must be greater than post timestamp
        delta_hours=random.randint(0, 100)
        if parent_id is None:
            parent_id = random.randint(1, 50)
        reply = Reply.query.filter_by(id=parent_id).first()
        timestamp = reply.timestamp + datetime.timedelta(hours=delta_hours)
        # last_edited time must be greater than timestamp
        last_edited = timestamp + datetime.timedelta(hours=delta_hours)

        reply = Reply(
            body=body,
            votes=votes,
            timestamp=timestamp,
            last_edited=last_edited,
            user_id=user_id,
            post_id=None,
            accepted=False,
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
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

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

        if os.path.getsize(file_path) > 0:
            return filename  
        else:
            os.remove(file_path)

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
    create_fake_depth1_replies()
    print("Created 50 fake depth-1 replies")
    create_fake_depth2_replies()
    print("Created 50 fake depth-2 replies")
    # create replies depends on the depth-2 replies
    parent_id = random.randint(50, 100)
    create_fake_depth2_replies(parent_id=parent_id)
    print("Created 50 fake depth-3 replies")
    create_fake_vote()
    print("Created 50 fake votes")
    create_fake_profile_img()
    scenario1()
    print("Created scenario1 data")
    scenario2()
    print("Created scenario2 data")