# -*- coding: utf8 -*-
"""
@summary:
@author: Zero
@date: 2023年8月1日
"""
import os
import threading

from PyQt6.QtCore import QStandardPaths
from PyQt6.QtWidgets import QWidget, QMessageBox

from backup.common.backup import BackupUtil
from backup.common.util import is_subdirectory
from backup.common.widgets import CommonMessageBox
from backup.core.custom_file_dialog import get_file_or_dir
from backup.view.path_wgt import Ui_PathWidget


class PathWidget(QWidget, Ui_PathWidget):
    def __init__(self, parent=None, index=0):
        super(PathWidget, self).__init__(parent=parent)
        self.setupUi(self)

        # 重要： index 索引，用于界面上移除配置时候定位
        self.index = index

        self.bind_events()

    def bind_events(self):
        self.pushButton_choose_source.clicked.connect(self.on_choose_path)
        self.pushButton_choose_target.clicked.connect(self.on_choose_path)

        self.pushButton_backup.clicked.connect(self.on_backup)
        self.pushButton_remove.clicked.connect(self.on_remove_path)
        self.textEdit_filter.textChanged.connect(self.on_text_changed)

    def get_backup_filter(self):
        """
        获取过滤器及去重
        :return:
        """
        backup_filter = self.textEdit_filter.toPlainText().strip()
        if backup_filter:
            backup_filter = [item.strip() for item in backup_filter.split('\n') if item.strip()]

        backup_filter = list(set(backup_filter))
        if not backup_filter:
            self.textEdit_filter.setPlainText('')
            return []

        self.textEdit_filter.setPlainText("\n".join(backup_filter))
        return backup_filter

    def on_choose_path(self):
        # 打开文件对话框
        # 尝试获取我的文档目录
        default_path = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.DocumentsLocation)
        default_path = default_path[0] if default_path else "./"

        data_path = get_file_or_dir(self, caption="选择文件夹或文件", directory=default_path)
        if not data_path or not isinstance(data_path, list):
            return
        data_path = data_path[0].strip()

        backup_filter = self.get_backup_filter()
        sender = self.sender()
        if sender == self.pushButton_choose_source:
            # 选择源
            self.lineEdit_source_path.setText(data_path)
            target_path = self.lineEdit_target_path.text().strip()
            if target_path and is_subdirectory(data_path, target_path):
                # 重置目标路径
                target_path = ''
                self.lineEdit_target_path.setText(target_path)

                icon = QMessageBox.Icon.Warning
                CommonMessageBox.show_message(self, text="请选择与源文件夹/文件目录不同的目标文件夹/文件", icon=icon)
                return

            self.window().config_util.update_path(data_path, target_path, backup_filter=backup_filter)
        elif sender == self.pushButton_choose_target:
            # 选择目标
            self.lineEdit_target_path.setText(data_path)
            source_path = self.lineEdit_source_path.text().strip()
            if source_path and is_subdirectory(source_path, data_path):
                # 重置目标路径
                data_path = ''
                self.lineEdit_target_path.setText(data_path)

                icon = QMessageBox.Icon.Warning
                CommonMessageBox.show_message(self, text="请选择与源文件夹/文件目录不同的目标文件夹/文件", icon=icon)
                return

            if source_path:
                self.window().config_util.update_path(source_path, data_path, backup_filter=backup_filter)

    def on_text_changed(self):
        backup_filter = self.textEdit_filter.toPlainText()
        if not backup_filter:
            return

        backup_filter = [item.strip() for item in backup_filter.split('\n') if item.strip()]
        backup_filter = list(set(backup_filter))

        source_path = self.lineEdit_source_path.text().strip()
        target_path = self.lineEdit_target_path.text().strip()
        if source_path and self.textEdit_filter.isEnabled():
            self.window().config_util.update_path(source_path, target_path, backup_filter=backup_filter)

    def on_remove_path(self):
        """
        移除备份配置
        :return:
        """
        source_path = self.lineEdit_source_path.text().strip()
        if source_path:
            self.window().config_util.remove_path(source_path)

        self.window().tab_widget.currentWidget().remove_widget(self)

    def on_backup(self):
        """
        备份数据
        1、校验源路径及目标路径是否合法；
        2、检查目标路径是否存在；
        3、开始备份，过滤指定目录及文件；
        :return:
        """
        source_path = self.lineEdit_source_path.text().strip()
        target_path = self.lineEdit_target_path.text().strip()
        if not source_path or not target_path:
            return

        source_path = os.path.abspath(source_path)
        target_path = os.path.abspath(target_path)

        if is_subdirectory(source_path, target_path):
            return

        if not os.path.exists(source_path):
            return

        # 获取过滤器
        backup_filter = self.get_backup_filter()
        backup_filter.extend(self.window().config_util.config['global_filters'])
        backup_filter = list(set(backup_filter))

        # 启动线程备份文件，稍后解决多次启动备份线程的问题
        threading.Thread(target=BackupUtil.backup,
                         args=(source_path, target_path, backup_filter)
                         ).start()
