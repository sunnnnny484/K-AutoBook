# --- coding: utf-8 ---
"""
A module for dmm books.
"""

import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from manager import AbstractManager


class Manager(AbstractManager):
    """
    A class for capturing dmm books.

    TODO only the first time is successful, after 2nd time got a failure first page. why?
    TODO reset to first page
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        Constructor for dmm books capturing.
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

        self._sleep(2)

        for i, w in enumerate(self.driver.window_handles):
            self.driver.switch_to.window(w)
            print(str(i) + " " + self.driver.current_url)
            if self.driver.current_url.startswith("https://book.dmm.com/streaming"):
                break

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

        self._sleep(2)

        # you need to reset the page to 1 on a browser also
        self._press_key(Keys.ARROW_RIGHT)
        self._sleep()
        self._press_key(Keys.ARROW_RIGHT)
        self._sleep()
        self._press_key(Keys.ARROW_RIGHT)
        self._sleep()

        # eliminate bar
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.click()
        self._sleep(2)

        self._set_total(total)
        for count in range(0, total):

            canvas = self.driver.find_elements(By.CSS_SELECTOR, f"#viewport{count % 2} > canvas")[0]
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
        for _ in range(Manager.MAX_LOADING_TIME):
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div#pageSliderCounter")
            print("_get_total_page: " + str(len(elements)))
            if len(elements) != 0:
                # print(f'{elements[0].get_attribute("innerHTML")}')
                if re.match('^\\d+/\\d+$', elements[0].get_attribute('innerHTML')):
                    return int(elements[0].get_attribute('innerHTML').split('/')[1])
            time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        Gets the element that displays the page number of the currently displayed page.
        @return If there is an element displaying the page number, that element, otherwise None
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, "div#pageSliderCounter")
        if len(elements) != 0:
            return elements[0]
        return None

    def _get_current_page(self):
        """
        Gets current page.
        @return current page
        """
        # print(int(self.current_page_element.get_attribute('innerHTML')))
        return int(self._get_current_page_element().get_attribute('innerHTML').split('/')[0])

    def _next(self):
        """
        Proceeds to next page.
        """
        current_page = self._get_current_page()
        self._press_key(self.next_key)
        if self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() != current_page + 1:
                time.sleep(0.1)
