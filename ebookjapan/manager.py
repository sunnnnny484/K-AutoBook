# --- coding: utf-8 ---
"""
ebookjapanの操作を行うためのクラスモジュール
"""

import base64
import io
import re
import time
from PIL import Image
from retry import retry
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from manager import AbstractManager


class Manager(AbstractManager):
    """
    ebookjapanの操作を行うためのクラス

    TODO reset to first page
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        ebookjapanの操作を行うためのコンストラクタ
        @param driver selenium instance
        """
        super().__init__(driver, config, directory, prefix)

        self.next_key = Keys.ARROW_LEFT
        """
        Key to proceed to next page
        """
        self.previous_key = None
        """
        前のページに戻るためのキー
        """
        self.current_page_element = None
        """
        Element that displays the page number of the currently displayed page
        """
        self.retry_count = 0

    def _fix_window_size(self):
        canvas = self.driver.find_elements(By.CSS_SELECTOR, 'canvas')[0]

        w = 480
        h = 640

        self.driver.set_window_size(w, h)
        self._sleep(1)

        self.set_attribute(canvas, 'style', f'width: {w}px; height: {h}px;')
        self._sleep(1)

        height = int(canvas.get_attribute('height'))
        print(f'height: {height}')

        self.driver.set_window_size(w, height)
        self._sleep(1)

        style = canvas.get_attribute('style')
        style = re.sub(r'height:\s+\d+px;$', f'height: {height}px;', style)
        self.set_attribute(canvas, 'style', style)
        print(f'style: {style}')
        self._sleep()

        width = int(canvas.get_attribute('width'))
        print(f'width: {width}')

        self.driver.set_window_size(width, height)
        print(f'window: {width}x{height}')
        self._sleep(1)

        print(f"canvas: {canvas.get_attribute('width')}x{canvas.get_attribute('height')}")
        style = canvas.get_attribute('style')
        print(f'style: {style}')

        # self.set_font_size()

    def set_font_size(self):
        #
        touch = self.driver.find_element(By.CSS_SELECTOR, "div.viewer")
        touch.click()  # show slider
        self._sleep(2)

        touch = self.driver.find_element(By.CSS_SELECTOR, "#__layout > div > div.main > header > div.header__menu > ul > li:nth-child(3) > a > i")
        touch.click()  # show dialog
        self._sleep()

        touch = self.driver.find_element(By.CSS_SELECTOR, "a.btn.btn--ss")
        touch.click()  # show dialog
        self._sleep()

        touch = self.driver.find_element(By.CSS_SELECTOR, "div.modalbox__close > div > i")
        touch.click()  # show dialog
        self._sleep()

    def start(self, url=None):
        """
        Starts automatic screenshots of pages.
        @return an error message if the error occurs, or True if it succeeds
        """
        self._wait()

        # resize by option
        self._sleep(2)

        self.driver.switch_to.frame(0)
        self._fix_window_size()

        total = self._get_total_page()
        if total is None:
            return 'Failed to get total page number'

        excludes = self._get_blank_check_exclude_pages(total)
        print(f'excludes: {excludes}')

        self.current_page_element = self._get_current_page_element()
        if self.current_page_element is None:
            return 'Failed to get current page information'

        self._set_total(total)

        self._save_image(0, self._capture())

        self.driver.find_element(By.CSS_SELECTOR, 'body').click()
        self._press_key(self.next_key)
        self.pbar.update(1)

        # different size from cover
        self._fix_window_size()

        for _count in range(1, total):

            self.retry_count = 0
            self._save_image(_count, self._capture(_count in excludes))
            self.pbar.update(1)

            self._next()
            self._sleep()

        return True

    def _get_blank_check_exclude_pages(self, _total):
        return [(_total - 1 + p) if p <= 0 else p for p in self.sub_config.blank_check_excludes]

    def _get_total_page(self):
        """
        Gets total page count.
        First, move the footer in and out.
        @return the total number of pages on success, None on failure
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, '.footer__page-output > .total-pages')
        if len(elements) == 0:
            return None
        for _ in range(Manager.MAX_LOADING_TIME):
            if elements[0].get_attribute('innerHTML') != '0':
                return int(elements[0].get_attribute('innerHTML'))
            time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        Gets the element that displays the page number of the currently displayed page.
        @return If there is an element displaying the page number, that element, otherwise None
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, '.footer__page-output > output')
        if len(elements) != 0:
            return elements[0]
        print("*** NO CURRENT ELEMENT ***")
        return None

    def _get_current_page(self):
        """
        Gets current page.
        @return current page
        """
        try:
            return int(self.current_page_element.get_attribute('innerHTML')[:-2])
        except Exception:
            print("*** NO CURRENT PAGE ***")
            return 0

    @retry(tries=10, delay=1)
    def _capture(self, ignore_blank=False):
        """
        @param ignore_blank ignore mistaken capture or not
        """
        base64_image = self.driver.get_screenshot_as_base64()
        image = Image.open(io.BytesIO(base64.b64decode(base64_image)))
        if self._is_config_jpeg():
            image = image.convert('RGB')

        if self._is_blank_image(image, 255) or self._is_blank_image(image, 245):
            print(f' blank page detected {self.retry_count}')
            if not ignore_blank:
                if self.retry_count < self.sub_config.blank_check_giveup:
                    self.retry_count += 1
                    raise Exception
                else:
                    print(' give up checking, ignore blank')

        return image

    @staticmethod
    def _is_blank_image(image, color):
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                if r != color or g != color or b != color:
                        return False
        return True

    def _next(self):
        """
        Proceeds to next page.
        スペースで次のページにすすめるのでスペースキー固定
        """
        current_page = self._get_current_page()
        self._press_key(self.next_key)
        if self._get_current_page() and self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() and self._get_current_page() != current_page + 1:
                time.sleep(0.1)
