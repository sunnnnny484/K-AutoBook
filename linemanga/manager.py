# --- coding: utf-8 ---
"""
line-manga の操作を行うためのクラスモジュール
"""

import base64
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from manager import AbstractManager


class Manager(AbstractManager):
    """
    line-manga の操作を行うためのクラス
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        Constructor for line-manga capturing.
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

        total = self._get_total_page()
        if total is None:
            return 'Failed to get total page number'

        self.current_page_element = self._get_current_page_element()
        if self.current_page_element is None:
            return 'Failed to get current page information'

        # get original size
        canvas = self.driver.find_element(By.CSS_SELECTOR, "canvas.dummy")
        self.driver.set_window_size(int(canvas.get_attribute('width')),
                                    int(canvas.get_attribute('height')))
        print(f'size: {canvas.get_attribute("width")}x{canvas.get_attribute("height")}')

        self._sleep()

        self._set_total(total)
        for count in range(0, total):

            _base64_image = self.driver.get_screenshot_as_base64()
            self._save_image_of_bytes(count, base64.b64decode(_base64_image))
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
        for _ in range(Manager.MAX_LOADING_TIME):
            elements = self.driver.find_elements(By.CSS_SELECTOR, "span.fnViewerSliderNumTotal")
            if len(elements) != 0:
                # print(f'"{elements[0].get_attribute('innerHTML')}"')
                if re.match(r'^\d+$', elements[0].get_attribute('innerHTML').strip()):
                    return int(elements[0].get_attribute('innerHTML').strip())
            time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        Gets the element that displays the page number of the currently displayed page.
        @return If there is an element displaying the page number, that element, otherwise None
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, "b.fnViewerSliderNumCurrent")
        if len(elements) != 0:
            return elements[0]
        return None

    def _get_current_page(self):
        """
        Gets current page.
        @return current page
        """
        # print(int(self.current_page_element.get_attribute('innerHTML')))
        return int(self.current_page_element.get_attribute('innerHTML'))

    def _next(self):
        """
        Proceeds to next page.
        """
        current_page = self._get_current_page()
        self._press_key(self.next_key)
        if self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() != current_page + 1:
                time.sleep(0.1)
