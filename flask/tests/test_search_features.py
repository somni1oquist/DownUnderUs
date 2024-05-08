import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Post
from app.tools import search_posts
from flask_login import login_user
from werkzeug.security import generate_password_hash


class CombinedSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('test_config')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()
        cls.client = cls.app.test_client(use_cookies=True)

        # Setup users
        user = User(username='john', email='john@example.com', interested_topics='Pets', password_hash=generate_password_hash('testpassword'))
        db.session.add(user)
        db.session.commit()

        # Setup posts
        posts = [
            Post(title="Raspberry Chocolate Cake", body="Delicious and easy cake recipe needed.", topic="Food and Cooking", tags='safety, rural', user_id=user.id),
            Post(title="Caring for your Dog", body="Essential tips for dog care required.", topic="Pets", user_id=user.id),
            Post(title="Urban Gardening Essentials", body="Key techniques called for thriving gardens.", topic="Gardening", tags='grass', user_id=user.id),
        ]
        db.session.add_all(posts)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
    
    def test_search_by_content(self):
        pagination = search_posts(content="chocolate")
        results = pagination.items
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Raspberry Chocolate Cake")

    def test_search_by_topic_gardening(self):
        pagination = search_posts(topics=["Gardening"])
        results = pagination.items
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Urban Gardening Essentials')

    def test_search_by_topic_pets(self):
        pagination = search_posts(topics=["Pets"])
        results = pagination.items
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Caring for your Dog') 

    def test_search_with_sorting(self):
        pagination = search_posts(sort_by = 'timestamp_desc')
        results = pagination.items
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].title, 'Urban Gardening Essentials')

    def test_empty_search(self):
        pagination = search_posts()
        results = pagination.items
        self.assertEqual(len(results), 3)
    
    def test_search_view(self):
        response = self.client.get(url_for('index.search', query='gardens', sortBy="timestamp_desc", topics='Gardening', tags='grass', page=1))
        self.assertEqual(response.status_code, 200)
        # get the post body
        self.assertTrue('Key techniques called' in response.get_data(as_text=True))
        # get the post title
        self.assertTrue('Essentials' in response.get_data(as_text=True))
    
    # test non-login user visit secend search page
    def test_index_search_as_anonymous(self):
        self.client.get('/signout', follow_redirects=True)
        response = self.client.get(url_for('index.index', page=2))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign In' in response.get_data(as_text=True))
        self.assertIn('Unlock Full Access!', response.get_data(as_text=True))

    # test login-user can see the interested topics
    def test_index_search_as_authenticated(self):
        with self.app.test_request_context():
            with self.client:
                user = User.query.filter_by(username='john').first()
                login_user(user)
                response = self.client.get(url_for('index.index'))
                self.assertEqual(response.status_code, 200)
                self.assertIn('Caring for your Dog', response.get_data(as_text=True))
                self.assertTrue('Sign Out' in response.get_data(as_text=True))

    def test_index_search_authenticated_pagination(self):
        with self.app.test_request_context():
            with self.client:
                user = User.query.filter_by(username='john').first()
                login_user(user)
                response = self.client.get(url_for('index.index', page=999))
                self.assertEqual(response.status_code, 200)
                self.assertIn('No results found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()     