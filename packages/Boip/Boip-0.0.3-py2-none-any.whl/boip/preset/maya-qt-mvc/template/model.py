# -*- coding: utf-8 -*-
"""model
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import generators
from __future__ import division

from maya import cmds


class SampleLogic(object):
    def print_select_object_name(self):
        """選択中のオブジェクト名を出力する
        """
        selected_object = cmds.ls(selection=True)
        print(selected_object)
