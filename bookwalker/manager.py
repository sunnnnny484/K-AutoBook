# --- coding: utf-8 ---
"""
book-walker の操作を行うためのクラスモジュール

@see https://github.com/xuzhengyi1995/Bookwalker_Downloader
"""

import time
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from manager import AbstractManager


class Manager(AbstractManager):
    """
    book-walker の操作を行うためのクラス
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        book-walker の操作を行うためのコンストラクタ
        @param driver splinter のブラウザインスタンス
        """
        super().__init__(driver, config, directory, prefix)

        self.next_key = Keys.ARROW_LEFT
        """
        次のページに進むためのキー
        """

    def start(self, url=None):
        """
        ページの自動スクリーンショットを開始する
        @return エラーが合った場合にエラーメッセージを、成功時に True を返す
        """
        self._wait()

        self._wait_loading()

        total = self._get_total_page()
        if total is None:
            return '全ページ数の取得に失敗しました'

        self._sleep(2)

        # get original size
        canvas = self.driver.find_element(By.CSS_SELECTOR, "canvas.dummy")
        self.driver.set_window_size(int(canvas.get_attribute('width')),
                                    int(canvas.get_attribute('height')))
        print(f'size: {canvas.get_attribute("width")}x{canvas.get_attribute("height")}')

        self._sleep()

        self._set_total(total)
        for count in range(0, total):

            canvas = self.driver.find_element(By.CSS_SELECTOR, ".currentScreen canvas")
            self._save_image_of_web_element(count, canvas)
            self.pbar.update(1)

            self._next()
            self._sleep()

        return True

    def _get_total_page(self):
        """
        全ページ数を取得する
        最初にフッタの出し入れをする
        @return 取得成功時に全ページ数を、失敗時に None を返す
        """
        for _ in range(Manager.MAX_LOADING_TIME):
            elements = self.driver.find_elements(By.ID, 'pageSliderCounter')
            if len(elements) != 0:
                # print(elements[0].get_attribute('innerHTML'))
                if re.match('^\\d+/\\d+$', elements[0].get_attribute('innerHTML').strip()):
                    return int(elements[0].get_attribute('innerHTML').split('/')[1])
            time.sleep(1)
        return None

    def _next(self):
        """
        次のページに進む
        """
        self._press_key(self.next_key)
        self._wait_loading()

    def _wait_loading(self):
        WebDriverWait(self.driver, 30).until_not(lambda x: self._check_is_loading(
            x.find_elements(By.CSS_SELECTOR, ".loading")))

    @staticmethod
    def _check_is_loading(list_ele):
        is_loading = False
        for i in list_ele:
            if i.is_displayed() is True:
                is_loading = True
                break
        return is_loading
