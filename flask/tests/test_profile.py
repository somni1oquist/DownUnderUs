from datetime import datetime, timedelta, timezone
import unittest
from app import create_app, db
from app.models import Post, Reply, Title, User
from werkzeug.security import generate_password_hash, check_password_hash
from config import TestConfig

class ProfileTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config = TestConfig)  
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.user = User(username='testuser', email='test@example.com', password_hash=generate_password_hash('testpass'))
        db.session.add(self.user)
        db.session.commit()

        self.client = self.app.test_client(use_cookies=True)
        self.login()

        self.create_posts_and_replies(12)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_posts_and_replies(self, num_posts):
        for i in range(num_posts):
            post = Post(title=f'Test Post {i}', body='This is a test.', topic='Food and Cooking', user_id=self.user.id, 
                        timestamp=datetime.now(timezone.utc) - timedelta(days=i))
            db.session.add(post)
            db.session.commit()

            reply = Reply(body='This is a test reply.', user_id=self.user.id, timestamp=datetime.now(timezone.utc) - timedelta(days=i),
                        post_id=post.id)
            db.session.add(reply)
            db.session.commit()

    def login(self):
        return self.client.post('/auth/signin', json={
            'username': 'testuser',
            'password': 'testpass'
        })

    def test_profile_view(self):
        response = self.client.get(f'/profile/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', response.get_data(as_text=True))

    def test_edit_profile(self):
        data = {'username': 'updatedname', 'email': 'updated@example.com', 'suburb': 'UpdatedSuburb'}
        response = self.client.put('/profile/edit', json=data)
        self.assertEqual(response.status_code, 200)
        updated_user = db.session.query(User).get(self.user.id)
        self.assertEqual(updated_user.username, 'updatedname')
        self.assertEqual(updated_user.email, 'updated@example.com')
        self.assertEqual(updated_user.suburb, 'UpdatedSuburb')

    def test_change_password(self):
        data = {'currentPassword': 'testpass', 'newPassword': 'newpass123'}
        response = self.client.post('/profile/password', json=data)
        self.assertEqual(response.status_code, 200)
        updated_user = db.session.query(User).get(self.user.id)
        self.assertTrue(check_password_hash(updated_user.password_hash, 'newpass123'))

    def test_change_password_incorrect_current(self):
        data = {'currentPassword': 'wrongpass', 'newPassword': 'newpass123'}
        response = self.client.post('/profile/password', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Incorrect current password', response.get_data(as_text=True))

    def test_delete_image(self):
        self.user.profile_image = 'test_image.jpg'
        db.session.commit()
        response = self.client.delete('/profile/delete_image')
        self.assertEqual(response.status_code, 200)
        self.user = db.session.query(User).get(self.user.id) 
        self.assertIsNone(self.user.profile_image)

    def test_points_history(self):
        response = self.client.get(f'/profile/{self.user.id}/points_history')
        self.assertEqual(response.status_code, 200)

    def test_award_titles(self):
        response = self.client.get('/profile/check-and-award-title')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('titles_awarded', data)
        self.assertIn('Newcomer', data['titles_awarded'])

    def test_profile_top_ten_posts(self):
        response = self.client.get(f'/profile/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)

        # Assert that the most recent post is present and the oldest one is not
        self.assertIn('<h3>Recent 10 posts</h3>', data)
        self.assertIn('Test Post 0', data)  
        self.assertNotIn('Test Post 11', data)

    def test_profile_top_ten_interactions(self):
        response = self.client.get(f'/profile/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)

        # Assert that the most recent reply is present and the oldest one is not
        self.assertIn('<h3>Recent 10 interactions</h3>', data)
        self.assertIn('Test Post 0', data)  
        self.assertNotIn('Test Post 11', data)

if __name__ == '__main__':
    unittest.main()