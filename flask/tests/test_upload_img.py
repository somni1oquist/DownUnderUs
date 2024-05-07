from werkzeug.security import generate_password_hash
from app import create_app, db
from config import TestConfig
from app.models import User
import os
import json
import unittest
from app.enums import ResponseStatus



class UploadProfileimg(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config = TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Add sample users
        user_password = generate_password_hash('testpassword')
        self.user = User(username='testuser', email='test@example.com', password_hash=user_password)
        db.session.add(self.user)
        db.session.commit()

        self.client = self.app.test_client()
        self.signin('testuser', 'testpassword')


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

    def test_upload_profileimg(self):
        example_image = './app/static/images/icons8-bmo-48.png'
        with open(example_image, 'rb') as img:
            data={
                'image': (img, 'example_image.png')
            }
            response = self.client.post('/upload/1', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], ResponseStatus.SUCCESS)
        self.assertIn('url', response_data)
        self.assertTrue(os.path.exists(os.path.join(self.app.config['UPLOAD_FOLDER'], self.user.profile_image)))


