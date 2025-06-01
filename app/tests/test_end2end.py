from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.urls import reverse
import time

class UserLoginTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_login(self):
        self.driver.get(f'{self.live_server_url}/login/')
        self.driver.find_element(By.NAME, 'username').send_keys('test')
        self.driver.find_element(By.NAME, 'password').send_keys('test123456')
        self.driver.find_element(By.CSS_SELECTOR, 'form button[type="submit"]').click()
        time.sleep(1)

    def tearDown(self):
        self.driver.quit()