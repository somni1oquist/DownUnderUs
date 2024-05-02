import unittest
from app import create_app, db
from app.models import User, Post
from flask_login import login_user
from config import TestConfig
from werkzeug.security import generate_password_hash

class CreatePostTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config= TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

        # Create a user
        user_password = generate_password_hash('testpassword')
        self.user = User(username='testuser', email='test@example.com', password_hash=user_password)
        db.session.add(self.user)
        db.session.commit()

        # Log in the user
        with self.client:
            self.client.post('/auth/signin', json={
                'username': 'testuser',
                'password': 'testpassword'
            })
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_post_success(self):
        # Test with valid data
        response = self.client.post('/post/create', data={
            'title': 'Test Post',
            'body': 'This is a test post.',
            'topic': 'Food and Cooking',
            'location': 'Test location'
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn('post_id', response.get_json())
        post = Post.query.first()
        self.assertIsNotNone(post)

    def test_create_post_failure(self):
        # Test with incomplete data
        response = self.client.post('/post/create', data={
            'title': '',
            'body': ''
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.get_json())

if __name__ == '__main__':
    unittest.main()