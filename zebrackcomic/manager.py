# --- coding: utf-8 ---
"""
zebrack-comic の操作を行うためのクラスモジュール
"""

import re
import time
from retry import retry
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from manager import AbstractManager, get_file_content_chrome


class Manager(AbstractManager):
    """
    zebrack-comic の操作を行うためのクラス
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        Constructor for zebrack-comic capturing.
        @param driver selenium instance
        """
        super().__init__(driver, config, directory, prefix)

        self.next_key = Keys.ARROW_LEFT
        """
        Key to proceed to next page
        """
        self._current_page_element = None
        """
        Element that displays the page number of the currently displayed page
        """

    def start(self, url=None):
        """
        Starts automatic screenshots of pages.
        @return an error message if the error occurs, or True if it succeeds
        """
        self.driver.set_window_size(480, 640)

        self._wait()

        total = self._get_total_page()
        self._set_total(total)

        for count in range(0, total):

            img = self._get_img()
            self._save_image_of_bytes(count, get_file_content_chrome(self.driver, img.get_attribute('src')))
            self.pbar.update(1)

            self._next()
            self._sleep()

        return True

    @retry(tries=3, delay=1)
    def _get_img(self):
        return self.driver.find_element(By.XPATH, "//img[starts-with(@src, 'blob:')]")

    def _get_total_page(self):
        """
        Gets total page count.
        First, move the footer in and out.
        @return the total number of pages on success, None on failure
        """
        for _ in range(Manager.MAX_LOADING_TIME):
            try:
                element = self.driver.find_element(By.XPATH, "//*[@id='root']/section/div/div/div[3]/p")
                # print(element.get_attribute('innerHTML'))
                if re.match('^\\d+ / \\d+$', element.get_attribute('innerHTML')):
                    return int(element.get_attribute('innerHTML').split('/')[1].strip())
            except Exception:
                time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        Gets the element that displays the page number of the currently displayed page.
        @return If there is an element displaying the page number, that element, otherwise None
        """
        try:
            element = self.driver.find_element(By.XPATH, "//*[@id='root']/section/div/div/div[3]/p")
            return element
        except Exception:
            return None

    def _get_current_page(self):
        """
        Gets current page.
        @return current page
        """
        # print(int(self.current_page_element.html.split('/')[0]))
        return int(self._get_current_page_element().get_attribute('innerHTML').split('/')[0].strip())

    def _next(self):
        """
        Proceeds to next page.
        スペースで次のページにすすめるのでスペースキー固定
        """
        current_page = self._get_current_page()
        self._press_key(self.next_key)
        if self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() != current_page + 1:
                time.sleep(0.1)
