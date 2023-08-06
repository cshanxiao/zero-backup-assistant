import shutil
import time
from pathlib import Path

from watchdog.events import (
    FileSystemEventHandler,
    EVENT_TYPE_MOVED,
    EVENT_TYPE_DELETED,
    EVENT_TYPE_CREATED,
    EVENT_TYPE_MODIFIED,
    EVENT_TYPE_CLOSED,
    EVENT_TYPE_OPENED, PatternMatchingEventHandler,
)
from watchdog.observers import Observer


class PathChangedEventHandler(FileSystemEventHandler):
    def __init__(self, source_path, target_path):
        super(PathChangedEventHandler, self).__init__()
        self.source_path = Path(source_path).absolute()
        self.target_path = Path(target_path).absolute()

    def on_any_event(self, event):
        # 文件或目录发生变化时触发的处理逻辑
        print(f'Event type: {event.event_type}  Path: {event.src_path}')
        print(event.is_directory, event.is_synthetic, type(event.key), event.key)

        changed_path = Path(event.src_path).absolute()
        relative_path = changed_path.relative_to(self.source_path)
        target_path = self.target_path / relative_path
        print(target_path)

        if event.event_type == EVENT_TYPE_MOVED:
            pass
        elif event.event_type == EVENT_TYPE_DELETED:
            pass

        elif event.event_type == EVENT_TYPE_MODIFIED:
            if target_path.is_file():
                pass


class FileChangedEventHandler(PatternMatchingEventHandler):
    patterns = ["*.txt"]  # 监测的文件类型，可以使用通配符匹配多个文件

    def on_modified(self, event):
        print(f"File modified: {event.src_path}")


class FilePathObserver:
    def __init__(self, source_path, target_path):
        self.source_path = Path(source_path).absolute()
        self.target_path = Path(target_path).absolute()
        self.event_handler = PathChangedEventHandler(source_path, target_path)
        self.observer = Observer()

    def start(self):
        self.observer.schedule(self.event_handler, self.source_path, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def join(self):
        self.observer.join()


def test():
    # 监测的目标文件夹路径
    source_path = r'D:\source_path\eNSP插件\新建文件夹\fdsafs.txt'
    target_path = r'I:\test_backup1'

    # 创建观察者对象并启动
    observer = FilePathObserver(source_path, target_path)
    observer.start()

    try:
        # 持续运行，直到手动停止
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        # 停止观察者
        observer.stop()

    # 等待观察者线程结束
    observer.join()


if __name__ == '__main__':
    test()
