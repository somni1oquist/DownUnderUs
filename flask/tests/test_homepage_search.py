import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Post
from flask_login import login_user

class TestHomeSearch(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test_config')
        self.app.config['SERVER_NAME'] = 'localhost:5000'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        user = User(username='john', 
                    email='john@example.com',
                    interested_topics='Pets'
                    )

        db.session.add(user)
        db.session.commit()

        post1= Post(
            title='test post 1',
            body='This is a test 111.',
            user_id=user.id, 
            topic='Schools',
            tags='safety, rural'
        )
        post2= Post(
            title='test post 2',
            body='This is a test 222.',
            user_id=user.id, 
            topic='Pets',
            tags='dag, cat'

        )
        db.session.add_all([post1, post2])
        db.session.commit()

        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # test non-login user visit secend search page
    def test_index_as_anonymous(self):
        response = self.client.get(url_for('index.index', page=2))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign In' in response.get_data(as_text=True))
        self.assertIn('Unlock Full Access!', response.get_data(as_text=True))
    


    # test login-user can see the interested topics
    def test_index_as_authenticated_page1(self):
        with self.app.test_request_context(): 
            with self.client:
                user = User.query.filter_by(username='john').first()
                login_user(user)
                response = self.client.get(url_for('index.index'))
                self.assertEqual(response.status_code, 200)
                self.assertIn('test post 2', response.get_data(as_text=True))


    def test_index_as_authenticated_page2(self):
        with self.app.test_request_context(): 
            with self.client:
                user = User.query.filter_by(username='john').first()
                login_user(user)
                response = self.client.get(url_for('index.index', page=2))
                self.assertEqual(response.status_code, 200)
                self.assertIn('No results found', response.get_data(as_text=True))
