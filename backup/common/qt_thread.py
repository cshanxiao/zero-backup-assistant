from PyQt6.QtCore import QThread, QWaitCondition, QMutex, pyqtSignal, QMutexLocker

from backup.common.constant import SignalData, SignalType

from backup.common.logger import logger


class WorkerThread(QThread):
    # 定义一个自定义信号，可以在工作线程中发送信号给主线程
    thread_signal = pyqtSignal(SignalData)

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.is_pause = False
        # QWaitCondition() 用于多线程同步，一个线程调用 QWaitCondition.wait() 阻塞等待，
        # 直到另外一个线程调用 QWaitCondition.wake() 唤醒才继续往下执行
        self.cond = QWaitCondition()
        self.mutex = QMutexLocker(QMutex())  # 锁对象

        self.args = args
        self.kwargs = kwargs

        self.callback = None
        self.callback_times = 1
        self.callback_interval = 3

    def set_callback(self, callback, times=1, interval=3):
        self.callback = callback
        self.callback_times = times
        self.callback_interval = interval

    # 线程运行的逻辑
    def run(self):
        if not self.callback:
            return

        while self.callback_times > 0:
            with self.mutex:
                if self.is_pause:
                    self.cond.wait(self.mutex)
                try:
                    self.callback(*self.args, **self.kwargs)
                except Exception as err:
                    logger.error(f"callback excepted, err: {err}")
                self.callback_times -= 1
            self.sleep(self.callback_interval)

        data = SignalData(signal_type=SignalType.ThreadFinished.value)
        self.thread_signal.emit(data)

    # 线程暂停
    def pause(self):
        self.is_pause = True

    # 线程恢复
    def resume(self):
        self.is_pause = False
        self.cond.wakeAll()

    # 线程停止
    def stop(self):
        self.terminate()
