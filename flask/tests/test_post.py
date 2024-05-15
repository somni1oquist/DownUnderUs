import unittest
from app import create_app, db
from app.models import User, Post
from config import TestConfig
from werkzeug.security import generate_password_hash
from app.enums import ResponseStatus, ResponseMessage

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

        # Create a post for editing or deleting
        self.post = Post(title='Test Post', 
                    body='This is a test post.',
                    user_id=self.user.id,
                    topic='Food and Cooking',
                    location='Test location',
                    tags='#unittest,pytest')
        
        db.session.add(self.post)
        db.session.commit()

        # Log in the user
        with self.client:
            self.client.post('/auth/signin', json={
                'email': 'test@example.com',
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
            'location': 'Test location',
            'tags': 'unittest,pytest'
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

    def test_edit_post_success(self):
        response = self.client.put(
            f'/post/{self.post.id}/edit', 
            json={
                'title': 'Edited Test Post',
                'body': 'Edited Post Content',
                'location': None,
                'tags': None
            }, 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ResponseMessage.EDITED in response.get_json()['message'])

    def test_edit_post_failure(self):
        # Test with invalid data
        response = self.client.put(
            f'/post/{self.post.id}/edit', 
            json={
                'title': '',
                'body': '',
                'location': '',
                'tags': '#unittest'
            }, 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ResponseStatus.ERROR, response.get_json()['status'])

    def test_delete_post_success(self):
        response = self.client.delete(f'/post/{self.post.id}/delete')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ResponseMessage.DELETED in response.get_json()['message'])

    def test_delete_nonexistent_post(self):
        response = self.client.delete(f'/post/999/delete')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(ResponseStatus.ERROR, response.get_json()['status'])

if __name__ == '__main__':
    unittest.main()