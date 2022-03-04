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
        @param driver splinter のブラウザインスタンス
        """
        super().__init__(driver, config, directory, prefix)

        self.next_key = Keys.ARROW_LEFT
        """
        次のページに進むためのキー
        """
        self.previous_key = None
        """
        前のページに戻るためのキー
        """
        self.current_page_element = None
        """
        現在表示されているページのページ番号が表示されるエレメント
        """
        self.retry_count = 0

    def _fix_window_size(self):
        canvas = self.driver.find_elements_by_css_selector('canvas')[0]

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

    def start(self, url=None):
        """
        ページの自動スクリーンショットを開始する
        @return エラーが合った場合にエラーメッセージを、成功時に True を返す
        """
        self._wait()

        # resize by option
        self._sleep(2)

        self.driver.switch_to.frame(0)
        self._fix_window_size()

        total = self._get_total_page()
        if total is None:
            return '全ページ数の取得に失敗しました'

        excludes = self._get_blank_check_exclude_pages(total)
        print(f'excludes: {excludes}')

        self.current_page_element = self._get_current_page_element()
        if self.current_page_element is None:
            return '現在のページ情報の取得に失敗しました'

        self._set_total(total)

        self._save_image(0, self._capture())

        self.driver.find_element_by_css_selector('body').click()
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
        全ページ数を取得する
        最初にフッタの出し入れをする
        @return 取得成功時に全ページ数を、失敗時に None を返す
        """
        elements = self.driver.find_elements_by_css_selector('.footer__page-output > .total-pages')
        if len(elements) == 0:
            return None
        for _ in range(Manager.MAX_LOADING_TIME):
            if elements[0].get_attribute('innerHTML') != '0':
                return int(elements[0].get_attribute('innerHTML'))
            time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        現在表示されているページのページ数が表示されているエレメントを取得する
        @return ページ数が表示されているエレメントがある場合はそのエレメントを、ない場合は None を返す
        """
        elements = self.driver.find_elements_by_css_selector('.footer__page-output > output')
        if len(elements) != 0:
            return elements[0]
        print("*** NO CURRENT ELEMENT ***")
        return None

    def _get_current_page(self):
        """
        現在のページを取得する
        @return 現在表示されているページ
        """
        try:
            return int(self.current_page_element.get_attribute('innerHTML')[:-2])
        except:
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
        次のページに進む
        スペースで次のページにすすめるのでスペースキー固定
        """
        current_page = self._get_current_page()
        self._press_key(self.next_key)
        if self._get_current_page() and self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() and self._get_current_page() != current_page + 1:
                time.sleep(0.1)
