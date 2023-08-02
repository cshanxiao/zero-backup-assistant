# -*- coding: utf-8 -*-
"""
@summary:
@author: Zero
@date: 2023年8月1日
"""
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDialog, QTabWidget

import settings
from backup.common.config import ConfigUtil
from backup.view.main_dlg import Ui_Maindlg


class MainDialog(QDialog, Ui_Maindlg):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        Ui_Maindlg.__init__(self)
        self.setupUi(self)

        self.tab_widget = None
        self.tray_icon = None
        self.config_util = ConfigUtil()
        self.create_ui()

    def create_ui(self):
        self.resize(settings.FRAME_WIDTH, settings.FRAME_HEIGHT)

        self.setMaximumSize(QtCore.QSize(settings.FRAME_WIDTH, settings.FRAME_HEIGHT))
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        self.setWindowIcon(QtGui.QIcon(Path(settings.RESOURCE_PATH).joinpath("tray.png").as_posix()))

        self.setWindowTitle(settings.APP_NAME)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(QtCore.QRect(0, 0, settings.FRAME_WIDTH, settings.FRAME_HEIGHT))
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setIconSize(QtCore.QSize(32, 32))
        self.show_tabs()
        self.tab_widget.setCurrentIndex(0)

    def show_tabs(self):
        """
        @summary:
        """
        from backup.control.backup_wgt import BackupWidget
        tab_normal = BackupWidget(self)
        tab_normal.setObjectName("tab_backup")
        icon = QtGui.QIcon(Path(settings.RESOURCE_PATH).joinpath("ssh.png").as_posix())
        self.tab_widget.addTab(tab_normal, icon, "数据备份")

    def create_tray_icon(self):
        # 创建托盘图标
        action_restore = QAction('主界面(&H)', self, triggered=self.restore_window)
        action_quit = QAction('退出(&Q)', self, triggered=QtWidgets.QApplication.quit)

        menu = QtWidgets.QMenu(self)
        menu.addAction(action_restore)
        menu.addAction(action_quit)

        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())
        self.tray_icon.setContextMenu(menu)

        self.tray_icon.activated.connect(self.on_icon_activated)
        self.tray_icon.messageClicked.connect(self.on_tray_icon_clicked)

    def closeEvent(self, event):
        """
        :param event: 窗口关闭事件
        :return:
        """
        event.ignore()
        self.hide()
        self.show_tray_icon()

    def show_tray_icon(self):
        # 存在底层 bug，多次关闭窗口，界面和托盘图标同时隐藏，暂时通过每次重新创建图标解决
        self.create_tray_icon()
        self.tray_icon.show()
        icon = QtWidgets.QSystemTrayIcon.MessageIcon(QtWidgets.QSystemTrayIcon.MessageIcon.Information)
        self.tray_icon.showMessage(
            '备份助手提示',  # 标题
            '工具将继续在系统托盘中运行，\n要退出本工具，\n请在系统托盘的右键菜单中选择"退出"',  # 信息
            icon,  # 图标
            1 * 1000)  # 信息显示持续时间

    def restore_window(self):
        # 恢复打显示主界面
        self.tray_icon.hide()
        self.showNormal()

    def on_tray_icon_clicked(self):
        QtWidgets.QMessageBox.information(self, '提示', '单击恢复显示主界面')

    def on_icon_activated(self, reason):
        """
        处理托盘图标激活事件
        :param reason:
            ActivationReason.Trigger：单击左键
            ActivationReason.Context：单击右键
            ActivationReason.DoubleClick: 双击左键
            ActivationReason.MiddleClick：单击中键
            ActivationReason.Unknown：未知
        :return:
        """
        if reason in (QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick,
                      QtWidgets.QSystemTrayIcon.ActivationReason.MiddleClick):
            # 双击鼠标或单击鼠标中键，弹出气泡消息
            self.show_message()
        elif reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            # 单击恢复主界面
            self.restore_window()

    def show_message(self):
        # 显示气球信息
        icon = QtWidgets.QSystemTrayIcon.MessageIcon(QtWidgets.QSystemTrayIcon.MessageIcon.Information)
        self.tray_icon.showMessage(
            "提示",  # 标题
            "对图标点击右键，选择主界面菜单恢复窗口",  # 信息
            icon,  # 图标
            3 * 1000)  # 信息显示持续时间
