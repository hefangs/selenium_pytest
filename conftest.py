import datetime

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver





def pytest_configure(config):
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    log_file = f"./logs/{current_time}.log"
    config.option.log_file = log_file


@pytest.fixture(scope="class")
def my_fix(request):
    driver = webdriver.Edge()
    driver.get("https://music.163.com")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    request.cls.driver = driver  # 绑定到类
    request.cls.wait = wait      # 绑定到类
    yield
    driver.quit()
