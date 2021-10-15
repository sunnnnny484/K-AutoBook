# --- coding: utf-8 ---
"""
amazon の操作を行うためのクラスモジュール
"""

import re
import time
from selenium.webdriver.common.keys import Keys
from manager import AbstractManager


class Manager(AbstractManager):
    """
    amazon の操作を行うためのクラス
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        amazon の操作を行うためのコンストラクタ
        @param driver selenium のブラウザインスタンス
        """
        super().__init__(driver, config, directory, prefix)

        self.next_key = Keys.ARROW_LEFT
        """
        次のページに進むためのキー
        """
        self.current_page_element = None
        """
        現在表示されているページのページ番号が表示されるエレメント
        """

    def start(self, url=None):
        """
        ページの自動スクリーンショットを開始する
        @return エラーが合った場合にエラーメッセージを、成功時に True を返す
        """
        self._wait()
        # print("window: 905x1328")
        # self.driver.set_window_size(905, 1328)
        self._sleep(3)

        print("total")
        total = self._get_total_page()
        if not total:
            return '全ページ数の取得に失敗しました'

        self.current_page_element = self._get_current_page_element()
        if self.current_page_element is None:
            return '現在のページ情報の取得に失敗しました'

        print("click")
        touch = self.driver.find_element_by_css_selector("body")
        touch.click()  # show slider
        self._sleep(3)

        # get original size
        # canvas = self.driver.find_element_by_css_selector("canvas")
        # ww = int(canvas.get_attribute('width'))
        # wh = int(canvas.get_attribute('height'))
        # self.driver.set_window_size(ww, wh)
        # print(f'size: {ww}x{wh}')

        self._set_total(total)
        for count in range(0, total):

            img = self.driver.find_element_by_css_selector("div.ki-root > div > canvas")
            self._save_image_of_web_element(count, img)

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
        for _ in range(30):
            elements = self.driver.find_elements_by_css_selector('span#pageInfoTotalPage')
            if len(elements) != 0:
                print(elements[0].get_attribute('innerHTML'))
                if re.match('^\\d+$', elements[0].get_attribute('innerHTML')):
                    return int(elements[0].get_attribute('innerHTML'))
            time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        現在表示されているページのページ数が表示されているエレメントを取得する
        @return ページ数が表示されているエレメントがある場合はそのエレメントを、ない場合は None を返す
        """
        elements = self.driver.find_elements_by_css_selector('span#pageInfoCurrentPage')
        if len(elements) != 0:
            return elements[0]
        print("no current")
        return None

    def _get_current_page(self):
        """
        現在のページを取得する
        @return 現在表示されているページ
        """
        try:
            # print(f"cur: {int(self.current_page_element.get_attribute('innerHTML'))}")
            return int(self.current_page_element.get_attribute('innerHTML'))
        except:
            return 0

    def _next(self):
        """
        次のページに進む
        """
        current_page = self._get_current_page()
        self._press_next()
        if self._get_current_page() and self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() != current_page + 1:
               time.sleep(0.1)

    def _press_next(self):
        body = self.driver.find_element_by_tag_name('body')
        body.send_keys(self.next_key)
