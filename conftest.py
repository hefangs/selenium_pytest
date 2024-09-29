
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

@pytest.fixture(scope="class")
def setup(self):
    self.driver = webdriver.Edge()
    self.driver.get("https://music.163.com")
    self.driver.maximize_window()
    self.wait = WebDriverWait(self.driver, 10)
    yield
    self.driver.quit()