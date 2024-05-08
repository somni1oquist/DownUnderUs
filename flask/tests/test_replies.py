import unittest
from app import create_app, db
from app.models import User, Post, Reply, Vote
from app.enums import ResponseStatus, ResponseMessage
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

    def test_edit_reply(self):
        reply = Reply(body='Reply body', post_id=self.post.id, user_id=self.user.id)
        db.session.add(reply)
        db.session.commit()

        response = self.client.put(
            f'/post/{self.post.id}/reply/{reply.id}/edit',
            json={'body': 'Edited Reply body'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ResponseMessage.REPLY_EDITED in response.get_json()['message'])

    # def test_edit_reply_malicious(self):

    def test_delete_reply(self):
        reply = Reply(body='Reply body', post_id=self.post.id, user_id=self.user.id)
        db.session.add(reply)
        db.session.commit()

        response = self.client.delete(f'/post/{self.post.id}/reply/{reply.id}/delete')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ResponseMessage.REPLY_DELETED in response.get_json()['message'])

    def test_delete_nonexistent_reply(self):
        response = self.client.delete(f'/post/{self.post.id}/reply/999/delete')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(ResponseStatus.ERROR, response.get_json()['status'])
        
    def test_accept_reply(self):
        reply = Reply(body='Reply body', post_id=self.post.id, user_id=self.user.id)
        db.session.add(reply)
        db.session.commit()

        response = self.client.put(f'/post/{self.post.id}/reply/{reply.id}/accept')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ResponseMessage.REPLY_ACCEPTED in response.get_json()['message'])

    def test_accept_more_reply(self):
        first_reply = Reply(body='Reply body', post_id=self.post.id, user_id=self.user.id, accepted=0)
        second_reply = Reply(body='Reply body', post_id=self.post.id, user_id=self.user.id, accepted=1)
        db.session.add(first_reply)
        db.session.add(second_reply)
        db.session.commit()

        response = self.client.put(f'/post/{self.post.id}/reply/{first_reply.id}/accept')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(ResponseStatus.ERROR, response.get_json()['status'])

    def test_upvote_reply(self):
        # Create another user
        user_password = generate_password_hash('testpassword')
        another_user = User(username='another_user', email='another_user@example.com', password_hash=user_password)
        db.session.add(another_user)
        db.session.commit()

        # Create reply by another user
        reply = Reply(body='Reply body', post_id=self.post.id, user_id=another_user.id)
        db.session.add(reply)
        db.session.commit()

        response = self.client.post(f'/post/{self.post.id}/reply/{reply.id}/vote', json={
            'vote': 'upvote'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ResponseMessage.VOTED, response.get_json()['message'])

    def test_upvote_reply_yourself(self):
        # Create reply by current user
        reply = Reply(body='Reply body', post_id=self.post.id, user_id=self.user.id)
        db.session.add(reply)
        db.session.commit()

        response = self.client.post(f'/post/{self.post.id}/reply/{reply.id}/vote', json={
            'vote': 'upvote'
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(ResponseStatus.ERROR, response.get_json()['status'])
    
    def test_revoke_reply(self):
        # Create another user
        user_password = generate_password_hash('testpassword')
        another_user = User(username='another_user', email='another_user@example.com', password_hash=user_password)
        db.session.add(another_user)
        db.session.commit()

        # Create reply by another user
        reply = Reply(body='Reply body', post_id=self.post.id, user_id=another_user.id)
        db.session.add(reply)
        db.session.commit()

        # Create vote record from current user
        vote = Vote(user_id=self.user.id, reply_id=reply.id, vote_type='upvote')
        db.session.add(vote)
        db.session.commit()

        response = self.client.post(f'/post/{self.post.id}/reply/{reply.id}/vote', json={
            'vote': 'downvote'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ResponseMessage.VOTE_REVOKED, response.get_json()['message'])


if __name__ == '__main__':
    unittest.main()
