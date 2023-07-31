# -*- coding: utf-8 -*-
"""
Created on 2014-1-2

@author: Zero
"""
from pathlib import Path

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QDialog, QTabWidget

import settings
from backup.control.backup_wgt import BackupWidget
from backup.view.main_dlg import Ui_Maindlg


class MainDialog(QDialog, Ui_Maindlg):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        Ui_Maindlg.__init__(self)
        self.setupUi(self)
        self.create_ui()

    def create_ui(self):
        self.resize(settings.FRAME_WIDTH, settings.FRAME_HEIGHT)
        self.setMaximumSize(QtCore.QSize(settings.FRAME_WIDTH, settings.FRAME_HEIGHT))
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        self.setWindowIcon(QtGui.QIcon(Path(settings.RESOURCE_PATH).joinpath("tray.png").as_posix()))

        self.setWindowTitle(settings.APP_NAME)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, settings.FRAME_WIDTH, settings.FRAME_HEIGHT))
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setIconSize(QtCore.QSize(32, 32))
        self.show_tabs()
        self.tabWidget.setCurrentIndex(0)

    def show_tabs(self):
        """
        @summary:
        """
        tab_normal = BackupWidget(self)
        tab_normal.setObjectName("tab_normal")
        icon = QtGui.QIcon(Path(settings.RESOURCE_PATH).joinpath("ssh.png").as_posix())
        self.tabWidget.addTab(tab_normal, icon, "数据备份")
