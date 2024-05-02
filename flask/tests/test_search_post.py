import unittest
from app import create_app, db
from app.models import User, Post
from app.tools import search_posts
from config import TestConfig
from datetime import datetime
from werkzeug.security import generate_password_hash

class SearchPostsTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config = TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Add sample users and posts
        user1 = User(
            username = 'user1',
            email = 'user1@example.com',
            password_hash = generate_password_hash('user1password'),
            suburb = 'Perth'
        )

        user2 = User(
            username = 'user2',
            email = 'user2@example.com',
            password_hash = generate_password_hash('user2password'),
            suburb = 'Fremantle'
        )

        db.session.add_all([user1, user2])
        db.session.commit()

        # Create posts linked to the users
        post1 = Post(title="Raspberry Chocolate Cake", body="Delicious and easy cake recipe needed.", 
                     topic = "Food and Cooking", user_id = user1.id)
        post2 = Post(title="Caring for your Dog", body="Essential tips for dog care required.", 
                     topic = "Pets", user_id = user2.id)
        post3 = Post(title="Urban Gardening Essentials", body="Key techniques called for thriving gardens.", 
                     topic = "Gardening", user_id = user2.id)
        db.session.add_all([post1, post2, post3])
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_by_content(self):
        results = search_posts(content="chocolate")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Raspberry Chocolate Cake")

    def test_search_by_topic_gardening(self):
        results = search_posts(topics=["Gardening"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Urban Gardening Essentials')

    def test_search_by_topic_pets(self):
        results = search_posts(topics=["Pets"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Caring for your Dog') 

    def test_search_with_sorting(self):
        results = search_posts(sort_by = 'timestamp_desc')
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['title'], 'Urban Gardening Essentials')

    def test_empty_search(self):
        results = search_posts()
        self.assertEqual(len(results), 3)

if __name__ == '__main__':
    unittest.main()
