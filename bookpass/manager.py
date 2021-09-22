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
        bookpass の操作を行うためのコンストラクタ
        @param driver splinter のブラウザインスタンス
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

        canvas = self.driver.find_element_by_css_selector("div.page > canvas")[0]
        self.driver.set_window_size(int(canvas.get_attribute('width')),
                                           int(canvas.get_attribute('height')))
        print(f'size: {canvas.get_attribute("width")}x{canvas.get_attribute("height")}')

        self._skip_first_dialog()
        self._sleep()

        touch = self.driver.find_element_by_css_selector("div.Viewer-fit-fill")
        touch.click()  # show slider
        self._sleep()

        total = self._get_total_page()
        if not total:
            return '全ページ数の取得に失敗しました'

        self.current_page_element = self._get_current_page_element()
        if self.current_page_element is None:
            return '現在のページ情報の取得に失敗しました'

        touch = self.driver.find_element_by_css_selector("body")
        touch.click()  # hide slider
        self._sleep()

        self._set_total(total)
        for count in range(0, total):

            canvas = self.driver.find_element_by_css_selector("div.page > canvas")
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
        elements = self.driver.find_elements_by_css_selector('span.maxIndexLabel')
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
        現在表示されているページのページ数が表示されているエレメントを取得する
        @return ページ数が表示されているエレメントがある場合はそのエレメントを、ない場合は None を返す
        """
        elements = self.driver.find_elements_by_css_selector('span.indexLabel')
        if len(elements) != 0:
            return elements[0]
        print("no current")
        return None

    def _get_current_page(self):
        """
        現在のページを取得する
        @return 現在表示されているページ
        """
        return int(self.current_page_element.get_attribute('innerHTML'))

    def _skip_first_dialog(self):
        """
        skip help dialog
        """
        elements = self.driver.find_elements_by_css_selector('button.Btn_cancel')
        if len(elements) != 0 and '見ない' in elements[0].get_attribute('innerHTML'):
            print('first dialog found, skip...')
            elements[0].click()
        else:
            print('first dialog not found')

    def _next(self):
        """
        次のページに進む
        """
        current_page = self._get_current_page()
        self._press_key(self.next_key)
        if self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() != current_page + 1:
                time.sleep(0.1)
