# --- coding: utf-8 ---
"""
amazon の実行クラスモジュール
"""

from runner import DirectPageRunner
from amazon.manager import Manager


class Runner(DirectPageRunner):
    """
    amazon の実行クラス
    https://read.amazon.co.jp/manga/B00JR0Q0YO?ref_=dbs_ebk_wr_lft
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, manager_class=Manager)
