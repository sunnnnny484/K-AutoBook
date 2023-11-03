# --- coding: utf-8 ---
"""
A module for piccoma runner.
"""

from piccoma.manager import Manager
from runner import DirectPageRunner


class Runner(DirectPageRunner):
    """
    A class for piccoma runner.
    https://piccoma.com/web/viewer/4267/1471900
    """

    def __init__(self, type_, driver, config):
        super().__init__(type_, driver, config, manager_class=Manager)

