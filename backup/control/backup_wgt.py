# -*- coding: utf8 -*-
u"""
@summary:
@author: Zero
@date: 2016年2月18日
"""
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDialog, QMessageBox, QSystemTrayIcon, QMenu, QApplication, QGroupBox, QLabel, QComboBox, \
    QStyle, QSpinBox, QPushButton, QTextEdit, QGridLayout, QLineEdit

from backup.control.path_wgt import PathWidget
from backup.view.backup_wgt import Ui_BackupWidget


class BackupWidget(QDialog, Ui_BackupWidget):
    def __init__(self, parent=None):
        super(BackupWidget, self).__init__(parent=parent)
        self.setupUi(self)

        self.bind_events()

    def bind_events(self):
        self.btn_add_path.clicked.connect(self.add_path)
        self.btn_realtime_backup.clicked.connect(self.realtime_backup)

    def add_path(self):
        widget = PathWidget(parent=self)
        self.verticalLayout_path.addWidget(widget)

    def realtime_backup(self):
        # 实时备份
        # 让托盘图标显示在系统托盘上
        self.window().hide()
        self.window().tray_icon.show()
