# --- coding: utf-8 ---
"""
line-manga の実行クラスモジュール
"""

import time
from config import SubConfigWithCookie
from os import path
from datetime import datetime
from runner import AbstractRunner
from linemanga.login import LineLogin
from linemanga.manager import Manager


class Runner(AbstractRunner):
    """
    line-manga の実行クラス
    https://manga.line.me/book/viewer?id=92dc0b4e-c5d4-4518-9fba-d78fb1e6b0f0
    """

    def __init__(self, type_, browser, config):
        super().__init__(type_, browser, config, SubConfigWithCookie)

    def run(self):
        """
        line-manga の実行
        """
        if self._set_cookie():
            self.driver.get('https://manga.line.me/store/')
            time.sleep(1)
        print('Loading page of inputted url (%s)' % self.url)
        self.browser.visit(self.url)

        print('Open main page')

        destination = self.get_output_dir()
        print(f'Output Path : {destination}')

        manager = Manager(
            self.browser, self.sub_config, destination)
        result = manager.start()
        if result is not True:
            print(result)
        return
