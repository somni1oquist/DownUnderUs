import unittest
from app import create_app, db
from app.models import User, Post, Reply
from config import TestConfig
from flask_login import current_user
from werkzeug.security import generate_password_hash

class ReplyTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config=TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a user
        user_password = generate_password_hash('testpassword')
        self.user = User(username='testuser', email='test@example.com', password_hash=user_password)
        db.session.add(self.user)
        db.session.commit()

        # Sign in the user
        self.client = self.app.test_client()
        self.signin('testuser', 'testpassword')

        # Create a post
        self.post = Post(title='Test Post', body='This is a test post.', user_id=self.user.id, topic='Food and Cooking')
        db.session.add(self.post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def signin(self, username, password):
        response = self.client.post('/auth/signin', json={
            'username': username,
            'password': password
        })
        return response

    def test_reply_to_post(self):
        response = self.client.post(f"/post/{self.post.id}/reply", json={
            'body': 'This is a reply to a post'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Reply.query.count() == 1)
        self.assertIsNone(Reply.query.first().parent_id)

    def test_reply_to_reply(self):
        first_reply = Reply(body='First reply', post_id=self.post.id, user_id=self.user.id)
        db.session.add(first_reply)
        db.session.commit()

        response = self.client.post(f'/post/{self.post.id}/reply/{first_reply.id}', json={
            'body': 'This is a reply to a reply'
        })
        self.assertEqual(response.status_code, 201)
        new_reply = Reply.query.filter(Reply.parent_id == first_reply.id).first()

        self.assertIsNotNone(new_reply)
        self.assertEqual(new_reply.parent_id, first_reply.id)
        self.assertIsNone(new_reply.post_id)

    def test_reply_to_nonexistent_post(self):
        response = self.client.post('/post/999/reply', json={'body': 'This is a reply'})
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
