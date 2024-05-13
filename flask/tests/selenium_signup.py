import time
import unittest
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app import create_app, db
from app.models import User
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

    def test_flow_signup(self):
        # Click sign-in/sign-up link
        sign_in_btn = self.driver.find_element(By.LINK_TEXT, 'Sign In')
        sign_in_btn.click()
        sign_up_btn = self.driver.find_element(By.LINK_TEXT, 'Sign Up')
        sign_up_btn.click()

        user = User(username='test_user', email='test@example.com')
        username_input = self.driver.find_element(By.ID, 'username')
        username_input.send_keys(user.username)
        email_input = self.driver.find_element(By.ID, 'email')
        email_input.send_keys(user.email)
        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys('password')
        confirm_password_input = self.driver.find_element(By.ID, 'confirm-password')
        confirm_password_input.send_keys('password')
        sign_up_button = self.driver.find_element(By.ID, 'signUpButton')
        sign_up_button.click()

        self.wait_for_load_mask()

        # Wait for the select interested topics modal to show
        topics_modal = WebDriverWait(self.driver, SHORT_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "topicModalLabel"))
        )
        self.assertTrue(topics_modal.is_displayed())
        lmask = self.driver.find_element(By.CLASS_NAME, 'lmask')
        if (lmask.is_displayed()):
            self.wait_for_load_mask()
        
        topic_inputs = self.driver.find_elements(By.XPATH, "//input[@type='button']")[:5]
        topics_selected = [input.get_attribute('value') for input in topic_inputs]
        for input in topic_inputs:
            input.click()
        next_button = self.driver.find_element(By.ID, 'next')
        next_button.click()

        self.wait_for_load_mask()

        # Click user profile
        profile_link = self.driver.find_element(By.CSS_SELECTOR, 'li.login-item > a:first-child')
        profile_link.click()
        
        username_text = self.driver.find_element(By.CLASS_NAME, 'profile-name').text
        email_text = self.driver.find_element(By.CSS_SELECTOR, 'p.profile-detail:first-child span').text
        topics_badges = self.driver.find_elements(By.CSS_SELECTOR, '.profile-topics-tags span')
        
        self.assertEqual(user.username, username_text)
        self.assertEqual(user.email, email_text)
        self.assertEqual(len(topics_selected), len(topics_badges))
        for topic in topics_badges:
            self.assertIn(topic.text, topics_selected)
        
        time.sleep(SHORT_TIMEOUT)
