# -*- coding: utf-8 -*-
"""
This is the unittest for mlabtex.
"""
from __future__ import division, absolute_import, print_function

import unittest
from mlabtex import __version__


class Test(unittest.TestCase):
    def setUp(self):
        self.version = __version__

    def test_mlabtex(self):
        print(self.version)


if __name__ == "__main__":
    unittest.main()
