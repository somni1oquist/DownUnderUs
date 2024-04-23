from faker import Faker
import random
from app import db
from app.models import Post
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

