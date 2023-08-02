from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QMessageBox
)


class CommonMessageBox:

    @staticmethod
    def show_message(parent=None, title="提示", text="提示信息", timeout=1500,
                     icon=None, button=None):
        """

        :param parent: 父窗体，QWidget 对象
        :param title: 提示窗标题
        :param text: 提示内容
        :param timeout: 窗口显示时间，单位：毫秒
        :param icon: 提示图标，
        :param button: 按钮
        :return:
        """
        icon = icon or QMessageBox.Icon.Information
        button = button or QMessageBox.StandardButton.NoButton
        msg_box = QMessageBox(parent)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(button)
        QtCore.QTimer.singleShot(timeout, msg_box.close)
        msg_box.exec()
