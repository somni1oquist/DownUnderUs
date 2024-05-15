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
from app.models import User
from app.enums import Topic
from config import TestConfig

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
        
        # Start the server in a separate process
        multiprocessing.set_start_method("fork")
        self.server_process = multiprocessing.Process(target=self.app.run)
        self.server_process.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(options)
        self.driver.get(localhost)
        self.driver.maximize_window()

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

        # Enter email and password
        email_input = self.driver.find_element(By.ID, 'email')
        email_input.send_keys(self.user.email)
        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys('password')
        
        sign_in_btn = self.driver.find_element(By.ID, 'signInButton')
        sign_in_btn.click()

        self.wait_for_load_mask()
        lmask = self.driver.find_element(By.CLASS_NAME, 'lmask')
        if (lmask.is_displayed()):
            self.wait_for_load_mask()

        # Click on the create button
        create_btn = WebDriverWait(self.driver, SHORT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, 'create'))
        )
        create_btn.click()

        # Wait for the create modal to show
        create_modal = WebDriverWait(self.driver, SHORT_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "createModal"))
        )
        self.assertTrue(create_modal.is_displayed())

        # Enter title
        title_input = self.driver.find_element(By.NAME, 'title')
        title_input.send_keys('Test Post')
        # Click on the topic dropdown
        topic_dropdown = self.driver.find_element(By.CSS_SELECTOR, '#createModal .dropdown-toggle')
        topic_dropdown.click()
        # Select a random topic
        topic_items = self.driver.find_elements(By.CSS_SELECTOR, '#topic-list .dropdown-item')
        topic_selected = topic_items[random.randint(0, len(topic_items) - 1)]
        topic_selected.click()
        # Enter content
        content_input = self.driver.find_element(By.CSS_SELECTOR, '#createModal .ql-editor')
        content_input.send_keys('This is a test post')
        # Click Post button
        create_btn = self.driver.find_element(By.CSS_SELECTOR, '#createModal button[type="submit"]')
        create_btn.click()
        
        self.wait_for_load_mask()

        # Check if the post is displayed
        post_title = self.driver.find_element(By.ID, 'title')
        post_content = self.driver.find_element(By.CSS_SELECTOR, '#post .card-body').text

        self.assertEqual('Test Post', post_title.text)
        self.assertEqual('This is a test post', post_content)

        time.sleep(SHORT_TIMEOUT)