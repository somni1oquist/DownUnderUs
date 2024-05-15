import unittest
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
from config import TestConfig
from app.enums import ResponseMessage

class AuthTestCase (unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config= TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup(self):
        # Successful registration
        response = self.client.post('/auth/signup', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': '123456',
            'suburb': 'Perth'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue('Registration successful' in response.get_json()['message'])

        # User already exists
        response = self.client.post('/auth/signup', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': '123456',
            'suburb': 'Perth'
        })

        self.assertEqual(response.status_code, 409)
        self.assertTrue('An account with this email already exists' in response.get_json()['message'])

    def test_signin(self):
        # Create a user
        user = User(username='testuser', email='test@example.com', password_hash=
                    generate_password_hash('password'))
        db.session.add(user)
        db.session.commit()

        # Correct login
        response = self.client.post('/auth/signin', json={
            'email': 'test@example.com',
            'password': 'password'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ResponseMessage.LOGIN_SUCCESS in response.get_json()['message'])

        # Incorrect login
        response = self.client.post('/auth/signin', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 401)
        self.assertTrue(ResponseMessage.INCORRECT_CREDENTIALS in response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()