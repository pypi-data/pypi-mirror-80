# -*- coding: utf-8 -*-
"""view
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import generators
from __future__ import division

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2.QtWidgets import QMainWindow

from .gui import sample_gui


class View(MayaQWidgetBaseMixin, QMainWindow):
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)

        self.gui = sample_gui.Ui_{tool_name}WindowUI()
        self.gui.setupUi(self)
