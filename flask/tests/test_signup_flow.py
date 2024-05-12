import multiprocessing
import threading
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app, db
from config import TestConfig

class TestE2E(unittest.TestCase):
    def setUp(self):
        self.testApp = create_app(test_config= TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        # Add a user to the db

        self.server_thread = multiprocessing.Process(target=self.testApp.run)
        self.server_thread.start()
        # self.app_thread = threading.Thread(target=self.testApp.run, kwargs={"debug": False})
        # self.app_thread.start()

        # Initialize Selenium WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:5000')
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page_title(self):
        self.driver.get('http://127.0.0.1:5000')
        expected_title='Down Under Us'
        self.assertEqual(self.driver.title, expected_title)

    def test_sign_up_and_select_topics_flow(self):
        # Navigate to home page
        self.driver.get('http://127.0.0.1:5000')

        # Click on the "Sign In" link from the navigation bar
        sign_in_link_nav = self.driver.find_element(By.LINK_TEXT, 'Sign In')
        sign_in_link_nav.click()

        # Click on the "Sign Up" link from the sign-in page
        sign_up_link_sign_in = self.driver.find_element(By.LINK_TEXT, 'Sign Up')
        self.driver.execute_script("arguments[0].scrollIntoView();", sign_up_link_sign_in)
        self.driver.execute_script("arguments[0].click();", sign_up_link_sign_in)

        # Fill and submit the sign-up form
        username_input = self.driver.find_element(By.ID, 'username')
        username_input.send_keys('test_user')
        email_input = self.driver.find_element(By.ID, 'email')
        email_input.send_keys('test48@example.com')
        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys('password')
        confirm_password_input = self.driver.find_element(By.ID, 'confirm-password')
        confirm_password_input.send_keys('password')
        sign_up_button = self.driver.find_element(By.ID, 'signUpButton')
        sign_up_button.click()

        # Wait for the loading indicator to disappear
        WebDriverWait(self.driver, 10).until(
        EC.invisibility_of_element_located((By.ID, 'loading-indicator'))
        )

        # Wait for the select interested topics page to load
        topics_heading = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Select Your Interested Topics')]"))
        )
        self.assertTrue(topics_heading.is_displayed())

        # Select the first three topics
        topic_buttons = self.driver.find_elements(By.XPATH, "//input[@type='button']")[:5]
        for button in topic_buttons:
            button.click()

       # Click on the "Next" button
        next_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'next'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", next_button)
        self.driver.execute_script("arguments[0].click();", next_button)

        # Wait for the second loading indicator to disappear
        WebDriverWait(self.driver, 10).until(
        EC.invisibility_of_element_located((By.ID, 'loading-indicator'))
        )

        # Assert that the page displays the "TOP 5 Topics" text
        top_topics_text = self.driver.find_element(By.XPATH, "//div[@id='topic_box']//div[@class='box_head']")
        self.assertEqual(top_topics_text.text, "TOP 5 Topics")

if __name__ == '__main__':
    unittest.main()        