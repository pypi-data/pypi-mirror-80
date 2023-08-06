# -*- coding: utf-8 -*-
"""controller
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import generators
from __future__ import division

from . import view
from . import model


class Controller(object):
    def __init__(self):
        self.__view = view.View()
        self.__model = model.SampleLogic()
        self.setup_event()

    def setup_event(self):
        self.__view.gui.printSelectedObjectNameButton.clicked.connect(self.clicked_print_selected_object_name_button)

    def clicked_print_selected_object_name_button(self):
        self.__model.print_select_object_name()

    # ===============================================================
    # GUI Events.
    # ===============================================================
    def show_gui(self):
        """GUIを表示する
        """
        self.__view.show()

    def close_gui(self):
        """GUIを閉じる
        """
        self.__view.close()
