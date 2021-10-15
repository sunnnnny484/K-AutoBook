# --- coding: utf-8 ---
"""
d-library.jp
"""

import time
from selenium.webdriver.common.keys import Keys
from manager import AbstractManager
from tqdm import tqdm


class Manager(AbstractManager):
    """
    Manages 'd-library.jp' scraping.
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        Creates 'd-library.jp' manager.
        @param driver selenium instance
        """
        super().__init__(driver, config, directory, prefix)

        self.pbar = tqdm(bar_format='{n_fmt}/{total_fmt}')

        self.next_key = Keys.ARROW_LEFT
        """
        The key for next page.
        """
        self.current_percent_element = None
        """
        The element indicates current position.
        """

    def start(self, url=None):
        """
        Starts scraping.
        @return an error massage or True when succeed.
        """
        self.driver.set_window_size(960, 1280)

        self._wait()

        self._sleep(3)

        iframe = self.driver.find_element_by_id('binb')
        self.driver.switch_to.frame(iframe)

        count = 0
        flag = True
        while flag:

            img = self.driver.find_element_by_css_selector("#main_canvas2")
            self._save_image_of_web_element(count, img)

            self.pbar.update(1)

            flag = self._next()
            self._sleep()

            count += 1
        return True

    def _next(self):
        """
        Gets next page.
        """
        self._press_key(self.next_key)

        try:
            self.driver.find_element_by_id('lastPageFrame')
            return False
        except:
            return True
