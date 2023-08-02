from abc import abstractmethod

from PyQt6.QtCore import QThread, QWaitCondition, QMutex, pyqtSignal

from backup.common.constant import SignalData


class BaseThread(QThread):
    thread_signal = pyqtSignal(SignalData)

    def __init__(self, callback_times=1, callback_interval=3, *args, **kwargs):
        super(BaseThread, self).__init__()
        '''
        :param callback_times: int, 回调次数
        :param callback_interval: int，回调间隔，单位：秒
        '''
        self.is_pause = False

        # QWaitCondition() 用于多线程同步，一个线程调用 QWaitCondition.wait() 阻塞等待，
        # 直到另外一个线程调用 QWaitCondition.wake() 唤醒才继续往下执行
        self.cond = QWaitCondition()
        self.mutex = QMutex()  # 锁对象

        self.callback_times = callback_times
        self.callback_interval = callback_interval

        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    def callback(self):
        pass

    # 线程启动
    def run(self) -> None:
        while self.callback_times > 0:
            with self.mutex:
                if self.is_pause:
                    self.cond.wait(self.mutex)
                self.callback()
                self.callback_times -= 1

            QThread.sleep(self.callback_interval)

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
