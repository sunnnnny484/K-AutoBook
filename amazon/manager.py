# --- coding: utf-8 ---
"""
A module for amazon capturing.
"""

import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from manager import AbstractManager


class Manager(AbstractManager):
    """
    A class for amazon capturing.
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        Constructor for amazon capturing.
        @param driver selenium instance
        """
        super().__init__(driver, config, directory, prefix)

        self.next_key = Keys.ARROW_LEFT
        """
        Key to proceed to next page
        """
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
        # print("window: 905x1328")
        # self.driver.set_window_size(905, 1328)
        self._sleep(3)

        print("total")
        total = self._get_total_page()
        if not total:
            return 'Failed to get total page number'

        self.current_page_element = self._get_current_page_element()
        if self.current_page_element is None:
            return 'Failed to get current page information'

        print("click")
        touch = self.driver.find_element(By.CSS_SELECTOR, "body")
        touch.click()  # show slider
        self._sleep(3)

        # get original size
        # canvas = self.driver.find_element(By.CSS_SELECTOR, "canvas")
        # ww = int(canvas.get_attribute('width'))
        # wh = int(canvas.get_attribute('height'))
        # self.driver.set_window_size(ww, wh)
        # print(f'size: {ww}x{wh}')

        self._set_total(total)
        for count in range(0, total):

            img = self.driver.find_element(By.CSS_SELECTOR, "div.ki-root > div > canvas")
            self._save_image_of_web_element(count, img)

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
        for _ in range(30):
            elements = self.driver.find_elements(By.CSS_SELECTOR, 'span#pageInfoTotalPage')
            if len(elements) != 0:
                print(elements[0].get_attribute('innerHTML'))
                if re.match('^\\d+$', elements[0].get_attribute('innerHTML')):
                    return int(elements[0].get_attribute('innerHTML'))
            time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        Gets the element that displays the page number of the currently displayed page.
        @return If there is an element displaying the page number, that element, otherwise None
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'span#pageInfoCurrentPage')
        if len(elements) != 0:
            return elements[0]
        print("no current")
        return None

    def _get_current_page(self):
        """
        Gets current page.
        @return current page
        """
        try:
            # print(f"cur: {int(self.current_page_element.get_attribute('innerHTML'))}")
            return int(self.current_page_element.get_attribute('innerHTML'))
        except Exception:
            return 0

    def _next(self):
        """
        Proceeds to next page.
        """
        current_page = self._get_current_page()
        self._press_next()
        if self._get_current_page() and self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() != current_page + 1:
               time.sleep(0.1)

    def _press_next(self):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(self.next_key)
