"""
sukima の実行クラスモジュール
"""

from runner import DirectPageRunner
from sukima.manager import Manager


class Runner(DirectPageRunner):
    """
    sukima の実行クラス
    https://www.sukima.me/bv/t/BT0000185480/v/1/s/1/p/0
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, manager_class=Manager)

