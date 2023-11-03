# --- coding: utf-8 ---
"""
A module for comicwalker runner.
"""

from runner import DirectPageRunner
from comicwalker.manager import Manager


class Runner(DirectPageRunner):
    """
    A class for comic-walker runner.
    https://comic-walker.com/viewer/?tw=2&dlcl=ja&cid=KDCW_MF09000001010005_68
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, manager_class=Manager)
