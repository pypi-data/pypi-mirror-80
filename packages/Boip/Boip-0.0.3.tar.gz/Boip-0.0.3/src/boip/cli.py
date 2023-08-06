# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import generators
from __future__ import division

import argparse

from . import app

ARGUMENT_DESCRIPTION = """
BoilerPlate生成\n
テンプレートフォルダの追加や、自動テンプレートフォルダ作成など
"""

SEARCH_FLAVOR_TEXT = """
テンプレートフォルダ追加検索パス
"""


def _main():
    parser = argparse.ArgumentParser(description=ARGUMENT_DESCRIPTION)

    parser.add_argument("-s", "--search", help=SEARCH_FLAVOR_TEXT)
    args = parser.parse_args()

    _boip_question_creator = app.BoipQuestionCreator(args.search)
    _boip_question_creator.create_question()
