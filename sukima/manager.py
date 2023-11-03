"""
sukima の操作を行うためのクラスモジュール
"""

import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from manager import AbstractManager


class Manager(AbstractManager):
    """
    sukima の操作を行うためのクラス
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        Constructor for sukima capturing.
        @param driver selenium のブラウザインスタンス
        """
        super().__init__(driver, config, directory, prefix)

        self.current_page_element = None
        """
        Element that displays the page number of the currently displayed page
        """

    def start(self, url=None):
        """
        Starts automatic screenshots of pages.
        @return an error message if the error occurs, or True if it succeeds
        """
        self._wait()

        self.driver.set_window_size(480, 640)
        self._sleep()

        total = self._get_total_page()
        if not total:
            return 'Failed to get total page number'

        self.current_page_element = self._get_current_page_element()
        if self.current_page_element is None:
            return 'Failed to get current page information'

        self._set_total(total)
        for count in range(0, total):

            canvas = self.driver.find_elements(By.CSS_SELECTOR, f"div#div_{count + 1} > canvas")[0]
            self._save_image_of_web_element(count, canvas)

            self.pbar.update(1)

            self._next()
            self._sleep()

        return True

    def _get_total_page(self):
        """
        Gets total page count.
        First, move the footer in and out.
        @return the total number of pages on success, None on failure
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, '.noUi-tooltip')
        if len(elements) == 0:
            # print("no total")
            return None
        for _ in range(Manager.MAX_LOADING_TIME):
            # print(_elements[0].get_attribute('innerHTML'))
            if re.match('^\\d+ / \\d+$', elements[0].get_attribute('innerHTML')):
                return int(elements[0].get_attribute('innerHTML').split('/')[1].strip())
            time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        Gets the element that displays the page number of the currently displayed page.
        @return If there is an element displaying the page number, that element, otherwise None
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, '.noUi-tooltip')
        if len(elements) != 0:
            return elements[0]
        print("no current")
        return None

    def _get_current_page(self):
        """
        Gets current page.
        @return current page
        """
        # print(f"{int(self._get_current_page_element().get_attribute('innerHTML').split('/')[0].strip())}")
        return int(self._get_current_page_element().get_attribute('innerHTML').split('/')[0].strip())

    def _next(self):
        """
        Proceeds to next page.
        """
        current_page = self._get_current_page()
        body = self.driver.find_elements(By.CSS_SELECTOR, "body")[0]
        body.send_keys(Keys.ARROW_LEFT)
        if self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() != current_page + 1:
                time.sleep(0.1)
