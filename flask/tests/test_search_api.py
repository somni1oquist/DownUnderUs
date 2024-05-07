import unittest
from flask import url_for
from app import create_app, db
from app.models import Post, User

class SearchViewTest(unittest.TestCase):
    def setUp(self):

        self.app = create_app('test_config')
        self.app.config['SERVER_NAME'] = 'localhost:5000'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_view(self):

        user = User(username='john', email='john@example.com')

        db.session.add(user)
        db.session.commit()

        post=self.post = Post(
            title='test post',
            body='This is a test.',
            user_id=user.id, 
            topic='Schools',
            tags='safety, rural'
        )
        db.session.add(post)
        db.session.commit()

        response = self.client.get(url_for('index.search', query='test', sortBy="timestamp_desc", topics='Schools',tags='safety', page=1))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('test post' in response.get_data(as_text=True))
        self.assertTrue('This is a test.' in response.get_data(as_text=True))

