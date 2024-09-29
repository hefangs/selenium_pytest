import time
import cv2
import numpy as np
import requests
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestMusic163:
    @pytest.fixture(scope="class")
    def setup(self):
        self.driver = webdriver.Edge()
        self.driver.get("https://music.163.com")
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()

    def login(self, setup):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-action="login"]'))).click()
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_3xIXD0Q6'))).click()
        time.sleep(2)

        checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, 'j-official-terms')))
        if not checkbox.is_selected():
            checkbox.click()
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_3fo6oHZe'))).click()
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '密码登录'))).click()
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_2OT0mQUQ'))).send_keys('15000840699')
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sR89MU1J'))).send_keys('hf15000840699')
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_3fo6oHZe'))).click()
        time.sleep(2)

    def verify(self, setup):
        url_s = self.driver.find_element(By.CLASS_NAME, 'yidun_jigsaw').get_attribute('src')
        url_b = self.driver.find_element(By.CLASS_NAME, 'yidun_bg-img').get_attribute('src')
        headers = {'user-agent': 'Mozilla/5.0'}
        data_s = requests.get(url_s, headers=headers).content
        data_b = requests.get(url_b, headers=headers).content

        with open('pic_s.png', 'wb') as f:
            f.write(data_s)
        with open('pic_b.png', 'wb') as f:
            f.write(data_b)

        simg = cv2.imread('pic_s.png')
        bimg = cv2.imread('pic_b.png')
        s_img = cv2.cvtColor(simg, cv2.COLOR_BGR2GRAY)
        b_img = cv2.cvtColor(bimg, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(b_img, s_img, cv2.TM_CCOEFF_NORMED)
        index_max = np.argmax(result)
        y, x = np.unravel_index(index_max, result.shape)

        adjusted_x = x + 10
        ele = self.driver.find_element(By.XPATH, "//div[contains(@class, 'yidun_slider')]")
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(ele, xoffset=adjusted_x, yoffset=0).perform()
        time.sleep(1)

    def navigate(self, setup):
        links = ["排行榜", "歌单", "主播电台", "歌手", "新碟上架", "我的音乐", "关注"]
        for link in links:
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, link))).click()
            time.sleep(2)

    def test_music163(self, setup):
        self.login(setup)
        self.verify(setup)
        self.navigate(setup)
