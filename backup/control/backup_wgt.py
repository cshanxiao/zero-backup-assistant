# -*- coding: utf8 -*-
"""
@summary:
@author: Zero
@date: 2023年8月1日
"""
from PyQt6.QtWidgets import QDialog, QListWidgetItem

from backup.control.path_wgt import PathWidget
from backup.view.backup_wgt import Ui_BackupWidget


class BackupWidget(QDialog, Ui_BackupWidget):
    def __init__(self, parent=None):
        super(BackupWidget, self).__init__(parent=parent)
        self.setupUi(self)

        self.init()
        self.bind_events()

    def init(self):
        """
        根据配置参数，载入初始界面
        :return:
        """
        config = self.parent().config_util.config
        for item in config['backup_paths'].values():
            '''
            config 模板
            {
                'id': backup_id,
                'source_path': source_path,
                'target_path': target_path,
                'backup_filter': backup_filter
            }
            '''
            widget = PathWidget(parent=self, index=self.listWidget_path.count())
            # 初始化时，禁用 textEdit_filter 组件，避免触发其 textChanged 事件，引起异常
            widget.textEdit_filter.setEnabled(False)
            widget.lineEdit_source_path.setText(item['source_path'])
            widget.lineEdit_target_path.setText(item['target_path'])
            widget.textEdit_filter.setText('\n'.join(item['backup_filter']))
            widget.textEdit_filter.setEnabled(True)

            list_widget_item = QListWidgetItem()
            list_widget_item.setSizeHint(widget.size())
            self.listWidget_path.addItem(list_widget_item)
            self.listWidget_path.setItemWidget(list_widget_item, widget)

        # 自动调整组件大小
        self.listWidget_path.adjustSize()

    def bind_events(self):
        self.btn_add_path.clicked.connect(self.on_add_path)
        self.btn_realtime_backup.clicked.connect(self.on_realtime_backup)

    def on_add_path(self):
        """
        添加目录配置
        :return:
        """
        widget = PathWidget(parent=self, index=self.listWidget_path.count())
        item = QListWidgetItem()
        item.setSizeHint(widget.size())
        self.listWidget_path.addItem(item)
        self.listWidget_path.setItemWidget(item, widget)

    def remove_widget(self, widget):
        """
        :note: 实现复杂，待优化
        :param widget:
        :return:
        """
        for index in range(self.listWidget_path.count()):
            item_widget = self.listWidget_path.itemWidget(self.listWidget_path.item(index))
            if item_widget.index == widget.index:
                self.listWidget_path.takeItem(index)
                break

    def on_realtime_backup(self):
        """
        实时备份，让托盘图标显示在系统托盘上
        :return:
        """
        # self.window().hide()
        # self.window().tray_icon.show()
