
from typing import Union
import unittest

import flask_unittest
from _pytest import unittest
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app import app as create_app


class TestFoo(flask_unittest.LiveTestCase):
    driver: Union[Chrome, None] = None
    std_wait: Union[WebDriverWait, None] = None

    @classmethod
    def setUpClass(cls):
        # Initiate the selenium webdriver
        options = ChromeOptions()
        options.add_argument('--headless')
        cls.driver = Chrome(options=options)
        cls.std_wait = WebDriverWait(cls.driver, 5)

    @classmethod
    def tearDownClass(cls):
        # Quit the webdriver
        cls.driver.quit()

    def test_foo_with_driver(self):
        # Use self.driver here
        # You also have access to self.server_url and self.app
        # Example of using selenium to go to index page and try to find some elements (on a hypothetical app)
        self.driver.get(self.server_url)
        self.std_wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Register')))
        self.std_wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Log In')))


class test_endpoints()
