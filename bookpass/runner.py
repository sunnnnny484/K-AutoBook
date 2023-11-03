# --- coding: utf-8 ---
"""
bookpass の実行クラスモジュール
"""
from selenium.webdriver.common.by import By

from config import BasicSubConfig
from runner import AbstractRunner
from bookpass.manager import Manager


class Runner(AbstractRunner):
    """
    bookpass の実行クラス
    https://bookpass.auone.jp/pack/detail/?iid=BT000069318400100101&cs=top_freecomics_reco_670&pos=2&tab=1&ajb=3
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, BasicSubConfig)

    def run(self):
        """
        bookpass の実行
        """
        print('Loading page of inputted url (%s)' % self.url)
        self.driver.get(self.url)

        if self._move_main_page():
            print('Open main page')
        else:
            print('ページの取得に失敗しました')
            return

        destination = self.get_output_dir()
        print(f'Output Path : {destination}')

        manager = Manager(self.driver, self.sub_config, destination)
        result = manager.start()
        if result is not True:
            print(result)
        return

    def _move_main_page(self):
        """
        実際の本のページに移動する
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.button.view_button')
        if len(elements) != 0 and '読む' in elements[0].get_attribute('innerHTML'):
            elements[0].click()
            return True
        return False
