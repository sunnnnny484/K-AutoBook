# --- coding: utf-8 ---
"""
bookpass の操作を行うためのクラスモジュール
"""

import time
from selenium.webdriver.common.keys import Keys
from manager import AbstractManager


class Manager(AbstractManager):
    """
    bookpass の操作を行うためのクラス
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        Constructor for bookpass capturing.
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

        canvas = self.driver.find_element(By.CSS_SELECTOR, "div.page > canvas")[0]
        self.driver.set_window_size(int(canvas.get_attribute('width')),
                                           int(canvas.get_attribute('height')))
        print(f'size: {canvas.get_attribute("width")}x{canvas.get_attribute("height")}')

        self._skip_first_dialog()
        self._sleep()

        touch = self.driver.find_element(By.CSS_SELECTOR, "div.Viewer-fit-fill")
        touch.click()  # show slider
        self._sleep()

        total = self._get_total_page()
        if not total:
            return 'Failed to get total page number'

        self.current_page_element = self._get_current_page_element()
        if self.current_page_element is None:
            return 'Failed to get current page information'

        touch = self.driver.find_element(By.CSS_SELECTOR, "body")
        touch.click()  # hide slider
        self._sleep()

        self._set_total(total)
        for count in range(0, total):

            canvas = self.driver.find_element(By.CSS_SELECTOR, "div.page > canvas")
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
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'span.maxIndexLabel')
        if len(elements) == 0:
            # print("no total")
            return None
        for _ in range(Manager.MAX_LOADING_TIME):
            # print(elements[0].get_attribute('innerHTML'))
            if elements[0].get_attribute('innerHTML') != '{{ value + 1 }}':
                return int(elements[0].get_attribute('innerHTML'))
            time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        Gets the element that displays the page number of the currently displayed page.
        @return If there is an element displaying the page number, that element, otherwise None
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'span.indexLabel')
        if len(elements) != 0:
            return elements[0]
        print("no current")
        return None

    def _get_current_page(self):
        """
        Gets current page.
        @return current page
        """
        return int(self.current_page_element.get_attribute('innerHTML'))

    def _skip_first_dialog(self):
        """
        skip help dialog
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'button.Btn_cancel')
        if len(elements) != 0 and '見ない' in elements[0].get_attribute('innerHTML'):
            print('first dialog found, skip...')
            elements[0].click()
        else:
            print('first dialog not found')

    def _next(self):
        """
        Proceeds to next page.
        """
        current_page = self._get_current_page()
        self._press_key(self.next_key)
        if self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() != current_page + 1:
                time.sleep(0.1)
