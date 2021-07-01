# --- coding: utf-8 ---
"""
booklive の操作を行うためのクラスモジュール
"""

import re
import time
from selenium.webdriver.common.keys import Keys
from manager import AbstractManager
from PIL import Image


class Manager(AbstractManager):
    """
    booklive の操作を行うためのクラス
    """

    def __init__(self, browser, config=None, directory='./', prefix=''):
        """
        booklive の操作を行うためのコンストラクタ
        @param browser splinter のブラウザインスタンス
        """
        super().__init__(browser, config, directory, prefix)

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
        self.browser.driver.set_window_size(480, 640)

        self._wait()

        total = self._get_total_page()
        if not total:
            return '全ページ数の取得に失敗しました'

        self.current_page_element = self._get_current_page_element()
        if self.current_page_element is None:
            return '現在のページ情報の取得に失敗しました'

        self._set_total(total)
        for _count in range(0, total):

            imgs = self.browser.find_by_css(f"#content-p{_count + 1} div.pt-img img")
            images = [self._get_image_by_url(img._element.get_attribute('src')) for img in imgs]
            # print(f'images: {len(images)}')
            hb = images[-1].size[1]
            w = images[0].size[0]
            h = sum(self._get_height(image.size[1], hb, image == images[-1]) for image in images)
            dest = Image.new('RGB', (w, h))
            hh = 0
            for image in images:
                dest.paste(image, (0, hh, w, hh + image.size[1]))
                hh += self._get_height(image.size[1], hb, image == images[-1])
            self._save_image(_count, dest)

            self.pbar.update(1)

            self._next()
            self._sleep()

        return True

    @staticmethod
    def _get_height(height, base, last):
        """
        TODO without any reasons
        """
        if 534 <= base <= 536:  # 1600
            if last:
                base = 534
            else:
                base = 533
        elif base == 400:  # 1200
            pass
        elif base == 640:  # ?
            pass
        else:
            print(f'unknown base {base}')
        margin = height - base
        return height - margin

    def _get_total_page(self):
        """
        全ページ数を取得する
        最初にフッタの出し入れをする
        @return 取得成功時に全ページ数を、失敗時に None を返す
        """
        for _ in range(Manager.MAX_LOADING_TIME):
            _elements = self.browser.find_by_css('#menu_slidercaption')
            if len(_elements) != 0:
                print(_elements.first.html)
                if re.match('^\\d+/\\d+$', _elements.first.html):
                    return int(_elements.first.html.split('/')[1])
            time.sleep(1)
        return None

    def _get_current_page_element(self):
        """
        現在表示されているページのページ数が表示されているエレメントを取得する
        @return ページ数が表示されているエレメントがある場合はそのエレメントを、ない場合は None を返す
        """
        _elements = self.browser.find_by_css('#menu_slidercaption')
        if len(_elements) != 0:
            return _elements.first
        print("no current")
        return None

    def _get_current_page(self):
        """
        現在のページを取得する
        @return 現在表示されているページ
        """
        try:
            return int(self.current_page_element.html.split('/')[0])
        except:
            return 0

    def _next(self):
        """
        次のページに進む
        """
        current_page = self._get_current_page()
        self._press_key(self.next_key)
        if self._get_current_page() and self._get_current_page() < self.pbar.total - 1:
            while self._get_current_page() != current_page + 1:
                time.sleep(0.1)
