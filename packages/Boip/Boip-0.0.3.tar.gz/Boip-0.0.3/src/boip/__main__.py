# -*- coding: utf-8 -*-
"""boip entrypoints.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import generators
from __future__ import division
import sys
from boip.cli import _main

sys.dont_write_bytecode = True
if __name__ == "__main__":
    _main()
