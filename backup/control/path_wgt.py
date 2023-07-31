# -*- coding: utf8 -*-
u"""
@summary:
@author: Zero
@date: 2016年2月18日
"""

from PyQt6.QtWidgets import QWidget

from backup.core.custom_file_dialog import get_file_or_dir
from backup.view.path_wgt import Ui_PathWidget


class PathWidget(QWidget, Ui_PathWidget):
    def __init__(self, parent=None):
        super(PathWidget, self).__init__(parent=parent)
        self.setupUi(self)

        # 动态调整备份按钮高度
        self.pushButton_backup.setMinimumHeight(self.verticalLayout_path.sizeHint().height())

        self.bind_events()

    def bind_events(self):
        self.pushButton_choose_source.clicked.connect(self.choose_path)
        self.pushButton_choose_target.clicked.connect(self.choose_path)

        self.pushButton_backup.clicked.connect(self.backup)

    def choose_path(self):
        # 打开文件对话框
        data_path = get_file_or_dir(self, caption="选择文件夹或文件", directory="./")
        if not data_path or not isinstance(data_path, list):
            print('data path invalid', data_path)
            return
        data_path = data_path[0]

        sender = self.sender()
        if sender == self.pushButton_choose_source:
            # 选择源
            self.lineEdit_source_path.setText(data_path)
        elif sender == self.pushButton_choose_target:
            # 选择目标
            self.lineEdit_target_path.setText(data_path)

    def backup(self):
        """
        备份数据
        1、校验源路径及目标路径是否合法；
        2、检查目标路径是否存在；
        3、开始备份，过滤指定目录及文件；
        :return:
        """
        pass
