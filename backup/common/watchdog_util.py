import os
import shutil
import threading
import time
import traceback
from pathlib import Path

from watchdog.events import (
    FileSystemEventHandler,
    EVENT_TYPE_MOVED,
    EVENT_TYPE_DELETED,
    EVENT_TYPE_CREATED,
    EVENT_TYPE_MODIFIED,
    PatternMatchingEventHandler,
)
from watchdog.observers import Observer


class PathChangedEventHandler(FileSystemEventHandler):
    def __init__(self, source_path, target_path):
        super(PathChangedEventHandler, self).__init__()
        self.source_path = Path(source_path).absolute()
        self.target_path = Path(target_path).absolute()

        self.event = []
        threading.Thread(target=self.handle_event, daemon=True).start()

    def on_any_event(self, event):
        # NOTE: 待完善
        # 文件或目录发生变化时触发的处理逻辑
        if event.event_type == EVENT_TYPE_CREATED:
            return
        self.event.insert(0, event)

    def handle_event(self):
        while True:
            try:
                if len(self.event) <= 0:
                    time.sleep(1)
                    continue

                time.sleep(5)
                event = self.event.pop()
                # 文件或目录发生变化时触发的处理逻辑
                if event.event_type == EVENT_TYPE_CREATED:
                    continue

                print(f'\nEvent type: {event.event_type} Path: {event.src_path}')
                print('length', len(self.event))
                print('event', event.is_directory, event.is_synthetic, type(event.key), event.key)

                changed_path = Path(event.src_path).absolute()
                print('changed_path', changed_path)
                relative_path = changed_path.relative_to(self.source_path)
                target_path = self.target_path / relative_path
                print('target_path', target_path, target_path.is_file())

                if event.event_type == EVENT_TYPE_MOVED:
                    if target_path.exists():
                        target_path.unlink(missing_ok=True)

                elif event.event_type == EVENT_TYPE_DELETED:
                    if not target_path.exists():
                        continue
                    if target_path.is_file():
                        target_path.unlink()
                    else:
                        shutil.rmtree(target_path.as_posix())

                elif event.event_type == EVENT_TYPE_MODIFIED:
                    print('file EVENT_TYPE_MODIFIED')
                    try:
                        os.makedirs(target_path.parent.as_posix(), exist_ok=True)
                        if target_path.is_dir():
                            os.makedirs(target_path.as_posix(), exist_ok=True)
                            shutil.copytree(changed_path.as_posix(), target_path.as_posix(),
                                            ignore=None,
                                            dirs_exist_ok=True)
                            continue
                        shutil.copy(changed_path, target_path)
                    except PermissionError:
                        pass
            except:
                traceback.print_exc()


class FileChangedEventHandler(PatternMatchingEventHandler):
    patterns = ["*.txt"]  # 监测的文件类型，可以使用通配符匹配多个文件

    def on_modified(self, event):
        print(f"File modified: {event.src_path}")


class FilePathObserver:
    def __init__(self, source_path, target_path):
        self.source_path = Path(source_path).absolute()
        self.target_path = Path(target_path).absolute()

        if self.source_path.is_dir():
            self.event_handler = PathChangedEventHandler(source_path, target_path)
        else:
            self.event_handler = FileChangedEventHandler(source_path, target_path)
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
    source_path = r'D:\test_source_源'
    target_path = r'E:\test_target_目标'

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
