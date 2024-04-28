from faker import Faker
import random
from app import db
from app.models import Post, User
from app.enums import Topic

fake = Faker()
TAGS = [
    'urban', 'rural', 'education', 'public transport', 'infrastructure',
    'healthcare', 'sports', 'community', 'safety', 'technology',
    'environment', 'governance', 'culture', 'leisure', 'real estate'
]

def create_fake_posts(num_posts=50):
    for _ in range(num_posts):
        title = fake.sentence(nb_words=6)
        body = fake.text(max_nb_chars=200)
        views = random.randint(0, 1000)
        votes = random.randint(0, 100)
        user_id = random.randint(1, 10)  # Assuming we have 10 users
        topic = random.choice(list(Topic)).value
        tags = ', '.join(random.sample(TAGS, random.randint(2, 5)))
        post = Post(
            title=title,
            body=body,
            views=views,
            votes=votes,
            user_id=user_id,
            topic=topic,
            tags=tags
        )
        db.session.add(post)
    
    db.session.commit()

suburbs = [
    "Perth", "Armadale", "Bayswater", "Canning", "Cockburn", "Fremantle",
    "Gosnells", "Joondalup", "Kalamunda", "Kwinana", "Melville"
]
topic_values = [topic.value for topic in Topic]
def create_fake_users(num_users=10):
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


