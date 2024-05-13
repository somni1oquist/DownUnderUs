import time
import unittest
import multiprocessing
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import Post, User
from app.enums import Topic
from config import TestConfig
from selenium.webdriver.common.keys import Keys

localhost = f'http://{TestConfig.SERVER_NAME}/'
SHORT_TIMEOUT  = 2
TIMEOUT = 5
LONG_TIMEOUT = 10

class TestE2E(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        # Add a user
        user_password = generate_password_hash('password')
        interested_topics = ','.join([Topic.FOOD_AND_COOKING.value, Topic.PETS.value, Topic.RENTALS.value])
        self.user = User(username='test_user', email='test@example.com', password_hash=user_password, interested_topics=interested_topics)
        db.session.add(self.user)
        db.session.commit()

         # Create a post
        self.post = Post(title='Test Post', body='This is a test post.', user_id=self.user.id, topic='Food and Cooking')
        db.session.add(self.post)
        db.session.commit()
        
        # Start the server in a separate process
        multiprocessing.set_start_method("fork")
        self.server_process = multiprocessing.Process(target=self.app.run)
        self.server_process.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(options)
        self.driver.get(localhost)

    def tearDown(self):
        self.server_process.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def wait_for_load_mask(self):
        '''Wait for the loading mask to disappear'''
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "lmask"))
        )
        WebDriverWait(self.driver, 3*LONG_TIMEOUT).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'lmask'))
        )

    def test_flow_post(self):
        # Click sign-in
        sign_in_btn = self.driver.find_element(By.LINK_TEXT, 'Sign In')
        sign_in_btn.click()

        # Enter username and password
        username_input = self.driver.find_element(By.ID, 'username')
        username_input.send_keys(self.user.username)
        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys('password')
        
        sign_in_btn = self.driver.find_element(By.ID, 'signInButton')
        sign_in_btn.click()

        self.wait_for_load_mask()
        lmask = self.driver.find_element(By.CLASS_NAME, 'lmask')
        if (lmask.is_displayed()):
            self.wait_for_load_mask()

        # Click on search button
        search_input = self.driver.find_element(By.ID, 'search-body')
        search_input.send_keys('Test Post')
        search_input.send_keys(Keys.ENTER)

        self.wait_for_load_mask()
        lmask = self.driver.find_element(By.CLASS_NAME, 'lmask')
        if (lmask.is_displayed()):
            self.wait_for_load_mask()

        # Wait for search results to be visible
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'search-result-box'))
        )

        # Click on the post link
        post_link = self.driver.find_element(By.LINK_TEXT, 'Test Post')
        post_link.click()

        # Reply to the post
        reply_editor = self.driver.find_element(By.CLASS_NAME, 'ql-editor')
        reply_editor.click()
        reply_editor.send_keys('This is reply to the post.')
        send_reply_button = self.driver.find_element(By.CSS_SELECTOR, 'a[data-action="reply"]')
        send_reply_button.click()

        WebDriverWait(self.driver, LONG_TIMEOUT).until(
            EC.alert_is_present()
        )

        alert = self.driver.switch_to.alert
        alert.accept()  

        self.wait_for_load_mask()
        lmask = self.driver.find_element(By.CLASS_NAME, 'lmask')
        if (lmask.is_displayed()):
            self.wait_for_load_mask()

        reply = self.driver.find_element(By.CSS_SELECTOR, "div.reply")
        
        # Assert the reply text
        reply_text = reply.find_element(By.CSS_SELECTOR, ".card-text").text
        expected_reply_text = "This is reply to the post."  
        self.assertIn(expected_reply_text, reply_text, "The reply content does not match the expected text")
        
        # Assert the author's name
        author_name = reply.find_element(By.CSS_SELECTOR, ".author-name").text
        expected_author_name = "test_user" 
        self.assertEqual(author_name, expected_author_name, "The author name does not match")
