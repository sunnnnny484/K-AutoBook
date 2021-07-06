"""
sukima の操作を行うためのクラスモジュール
"""

import re
import time
from selenium.webdriver.common.keys import Keys
from manager import AbstractManager


class Manager(AbstractManager):
    """
    sukima の操作を行うためのクラス
    """

    def __init__(self, driver, config=None, directory='./', prefix=''):
        """
        sukima の操作を行うためのコンストラクタ
        @param driver selenium のブラウザインスタンス
        """
        super().__init__(driver, config, directory, prefix)

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

        # make ad clickable
        self.driver.set_window_size(1024, 640)
        self._sleep()

        touch = self.driver.find_elements_by_css_selector("div.popupad-box.text-center > div.text-center > div > a > div")[0]
        touch.click()  # hide ad
        self._sleep()

        self.driver.set_window_size(480, 640)
        self._sleep()

        total = self._get_total_page()
        if not total:
            return '全ページ数の取得に失敗しました'

        self.current_page_element = self._get_current_page_element()
        if self.current_page_element is None:
            return '現在のページ情報の取得に失敗しました'

        self._set_total(total)
        for count in range(0, total):

            canvas = self.driver.find_elements_by_css_selector(f"div#div_{count + 1} > canvas")[0]
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
        elements = self.driver.find_elements_by_css_selector('.noUi-tooltip')
        if len(elements) == 0:
            # print("no total")
            return None
        for _ in range(Manager.MAX_LOADING_TIME):
            # print(_elements[0].get_attribute('innerHTML'))
            if re.match('^\\d+ / \\d+$', elements[0].get_attribute('innerHTML')):
                return int(elements[0].get_attribute('innerHTML').split('/')[1].strip())
            time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        現在表示されているページのページ数が表示されているエレメントを取得する
        @return ページ数が表示されているエレメントがある場合はそのエレメントを、ない場合は None を返す
        """
        elements = self.driver.find_elements_by_css_selector('.noUi-tooltip')
        if len(elements) != 0:
            return elements[0]
        print("no current")
        return None

    def _get_current_page(self):
        """
        現在のページを取得する
        @return 現在表示されているページ
        """
        # print(f"{int(self._get_current_page_element().get_attribute('innerHTML').split('/')[0].strip())}")
        return int(self._get_current_page_element().get_attribute('innerHTML').split('/')[0].strip())

    def _next(self):
        """
        次のページに進む
        """
        current_page = self._get_current_page()
        body = self.driver.find_elements_by_css_selector("body")[0]
        body.send_keys(Keys.ARROW_LEFT)
        if self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() != current_page + 1:
                time.sleep(0.1)
