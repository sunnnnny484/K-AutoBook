# --- coding: utf-8 ---
"""
dmm books の実行クラスモジュール
"""

import time
from config import SubConfigWithCookie
from runner import AbstractRunner
from dmmbooks.manager import Manager


class Runner(AbstractRunner):
    """
    dmm books の実行クラス
    https://book.dmm.com/library/?item_id=b900qkds03987
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, SubConfigWithCookie)

    def run(self):
        """
        line-manga の実行
        """
        if self._set_cookie():
            self.driver.get('https://book.dmm.com/')
            time.sleep(1)
        print('Loading page of inputted url (%s)' % self.url)
        self.driver.get(self.url)

        if self._move_main_page():
            print('Open main page')
        else:
            print('ページの取得に失敗しました')
            return

        destination = self.get_output_dir()
        print(f'Output Path : {destination}')

        manager = Manager(
            self.driver, self.sub_config, destination)
        result = manager.start()
        if result is not True:
            print(result)
        return

    def _move_main_page(self):
        """
        実際の本のページに移動する
        """
        elements = self.driver.find_elements_by_css_selector('div.m-boxListBookProductBlock__btn > div')
        if len(elements) != 0 and '読む' in elements[0].text:
            elements[0].click()
            return True
        return False
