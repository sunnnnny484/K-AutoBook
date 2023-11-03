# --- coding: utf-8 ---
"""
gangan-online の操作を行うためのクラスモジュール
"""

from retry import retry
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
from manager import AbstractManager, get_file_content_chrome
from selenium.webdriver.common.by import By


class Manager(AbstractManager):
    """
    gangan-online の操作を行うためのクラス
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        Constructor for gangan-online capturing.
        @param driver selenium instance
        """
        super().__init__(driver, config, directory, prefix)

        self.pbar = tqdm(bar_format='{n_fmt}/{total_fmt}')

        self.next_key = Keys.ARROW_LEFT
        """
        Key to proceed to next page
        """

    def start(self, url=None):
        """
        Starts automatic screenshots of pages.
        @return an error message if the error occurs, or True if it succeeds
        """
        self._wait()

        self.driver.set_window_size(480, 640)

        count = 0
        while True:

            img = self._get_img()
            try:
                self.driver.find_element(By.XPATH, "//button[text() = '閉じる']")
                break
            except Exception:
                if count != 0:
                    self._save_image_of_bytes(count, get_file_content_chrome(self.driver, img.get_attribute('src')))
                    self.pbar.update(1)

                self._next()
                self._sleep()

                count = count + 1

        return True

    @retry(tries=3, delay=1)
    def _get_img(self):
        return self.driver.find_element(By.XPATH, "//img[starts-with(@src, 'blob:')]")

    def _next(self):
        """
        Proceeds to next page.
        """
        self._press_key(self.next_key)
