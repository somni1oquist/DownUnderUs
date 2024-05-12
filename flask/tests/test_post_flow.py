import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        driver_path = os.path.join(os.path.dirname(__file__), '../drivers/chromedriver')
        service = Service(executable_path=driver_path) 
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_sign_in_and_create_post(self):
        # Navigate to the sign-in page
        self.driver.get('http://127.0.0.1:5000')

        # Click on the "Sign In" link from the navigation bar
        sign_in_link_nav = self.driver.find_element(By.LINK_TEXT, 'Sign In')
        sign_in_link_nav.click()

        # Fill and submit the sign-in form
        username_input = self.driver.find_element(By.ID, 'username')
        username_input.send_keys('ras')  
        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys('test')  
        sign_in_button = self.driver.find_element(By.ID, 'signInButton')
        sign_in_button.click()

         # Wait for the loading indicator to disappear
        WebDriverWait(self.driver, 10).until(
        EC.invisibility_of_element_located((By.ID, 'loading-indicator'))
        )

        # Navigate to the pop-up to create a post
        create_post_link = self.driver.find_element(By.ID, 'create')
        create_post_link.click()

        # Wait for the create post modal to be displayed
        create_modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'createModal'))
        )

        # Fill out the form to create a post
        title_input = create_modal.find_element(By.ID, 'title')
        title_input.send_keys('Test Post')  

        # Select a topic from the dropdown
        topic_dropdown = create_modal.find_element(By.XPATH, '//button[text()="Please select a topic"]')
        topic_dropdown.click()
        topic_option = create_modal.find_element(By.XPATH, '//ul[@id="topic-list"]/li[1]')
        topic_option.click()
        quill_editor = self.driver.find_element(By.CLASS_NAME, 'ql-editor')
        quill_editor.click()
        quill_editor.send_keys('Test Post Body')

        # Submit the form
        submit_button = create_modal.find_element(By.XPATH, '//button[text()="Post"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        self.driver.execute_script("arguments[0].click();", submit_button)

         # Wait for the loading indicator to disappear
        WebDriverWait(self.driver, 10).until(
        EC.invisibility_of_element_located((By.ID, 'loading-indicator'))
        )

        # Wait for the new page to load and check for the edit post button
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'title-btn'))
    )
        title_element = self.driver.find_element(By.ID, 'title')
        created_post_title = title_element.text
        self.assertEqual(created_post_title, 'Test Post')

if __name__ == '__main__':
    unittest.main()
