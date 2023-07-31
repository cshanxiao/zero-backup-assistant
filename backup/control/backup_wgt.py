# -*- coding: utf8 -*-
u"""
@summary:
@author: Zero
@date: 2016年2月18日
"""

from PyQt6.QtWidgets import QDialog

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
        pass
