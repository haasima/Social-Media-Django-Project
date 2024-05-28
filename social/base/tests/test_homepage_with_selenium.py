from django.test import TestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TestHomepageWithSelenium(TestCase):
    def setUP(self):
        self.driver = webdriver.Chrome(ChromeDriverManager.install())
        
    def test_links(self):
        self.driver.get("http://127.0.0.1:8000/")
      #  self.driver.find_elements_by_class_name("navbar-brand").click()
        self.assertEqual("http://127.0.0.1:8000", self.driver.current_url)
        
    def tearDown(self):
        self.driver.quit