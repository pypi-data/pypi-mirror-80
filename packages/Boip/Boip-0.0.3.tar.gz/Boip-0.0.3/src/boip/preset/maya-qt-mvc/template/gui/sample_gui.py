# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets


class Ui_{tool_name}WindowUI(object):
    def setupUi(self, {tool_name}WindowUI):
        {tool_name}WindowUI.setObjectName("{tool_name}WindowUI")
        {tool_name}WindowUI.resize(265, 168)
        self.centralwidget = QtWidgets.QWidget({tool_name}WindowUI)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.printSelectedObjectNameButton = QtWidgets.QPushButton(self.centralwidget)
        self.printSelectedObjectNameButton.setObjectName("printSelectedObjectNameButton")
        self.gridLayout.addWidget(self.printSelectedObjectNameButton, 2, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        {tool_name}WindowUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar({tool_name}WindowUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 265, 21))
        self.menubar.setObjectName("menubar")
        {tool_name}WindowUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar({tool_name}WindowUI)
        self.statusbar.setObjectName("statusbar")
        {tool_name}WindowUI.setStatusBar(self.statusbar)

        self.retranslateUi({tool_name}WindowUI)
        QtCore.QMetaObject.connectSlotsByName({tool_name}WindowUI)

    def retranslateUi(self, {tool_name}WindowUI):
        {tool_name}WindowUI.setWindowTitle(QtWidgets.QApplication.translate("{tool_name}WindowUI", "{tool_name}Window", None, -1))
        self.printSelectedObjectNameButton.setText(QtWidgets.QApplication.translate("{tool_name}WindowUI", "Output the selected object name.", None, -1))
        self.textBrowser.setHtml(QtWidgets.QApplication.translate("{tool_name}WindowUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                                  "p, li { white-space: pre-wrap; }\n"
                                                                  "</style></head><body style=\" font-family:\'MS UI Gothic\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Thanks for installing Boip!</p></body></html>", None, -1))
