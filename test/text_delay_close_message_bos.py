from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer


def show_delayed_message():
    # 创建 QMessageBox 对话框
    msg_box = QMessageBox()
    msg_box.setWindowTitle("提示")
    msg_box.setText("这是一个延迟关闭的提示窗口")

    # 设置定时器
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(msg_box.close)
    timer.start(5000)

    # 显示对话框，并启动定时器
    msg_box.exec()


if __name__ == "__main__":
    app = QApplication([])
    show_delayed_message()
    app.exec()
