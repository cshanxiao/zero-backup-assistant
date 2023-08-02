from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox


class CommonMessageBox:

    @staticmethod
    def show_message(parent=None, title="提示", text="提示信息", timeout=3000,
                     icon=None, button=None):
        """
        可以延时关闭的提示窗口
        :param parent: 父窗体，QWidget 对象
        :param title: 提示窗标题
        :param text: 提示内容
        :param timeout: 窗口显示时间，单位：毫秒
        :param icon: 提示图标，
        :param button: 按钮
        :return:
        """
        icon = icon or QMessageBox.Icon.Information
        button = button or QMessageBox.StandardButton.Ok
        msg_box = QMessageBox(parent)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(button)

        # 设置定时器，延时关闭
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(msg_box.close)
        timer.start(timeout)

        msg_box.exec()
