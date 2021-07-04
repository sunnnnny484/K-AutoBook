# --- coding: utf-8 ---
"""
gangan-online の実行クラスモジュール
"""

from runner import DirectPageRunner
from ganganonline.manager import Manager


class Runner(DirectPageRunner):
    """
    gangan-online の実行クラス
    https://viewer.ganganonline.com/manga/?chapterId=15502
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, manager_class=Manager)
