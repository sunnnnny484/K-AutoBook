# --- coding: utf-8 ---
"""
A module for booklive runner.
"""

from runner import DirectPageRunner
from booklive.manager import Manager


class Runner(DirectPageRunner):
    """
    A class for booklive runner.
    https://booklive.jp/bviewer/s/?cid=208562_003&rurl=https%3A%2F%2Fbooklive.jp%2Findex%2Fno-charge%2Fcategory_id%2FC
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, manager_class=Manager)
