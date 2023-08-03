import hashlib
import os
import shutil
import time
import traceback
from pathlib import Path

from backup.common.eception import PathError, BackupError


def get_millisecond():
    return int(time.time() * 1000)


def is_subdirectory_py39(parent_dir, child_dir):
    """
    python 3.9 以上版本，判断 child_path 是否是 parent_path 的子目录
    :param parent_dir:
    :param child_dir:
    :return:
    """
    parent_path = Path(parent_dir).resolve()
    child_path = Path(child_dir).resolve()

    # 判断 child_path 是否是 parent_path 的子目录
    return child_path.is_relative_to(parent_path)


def is_subdirectory(parent_dir, child_dir):
    """
    判断 child_path 是否是 parent_path 的子目录
    :param parent_dir:
    :param child_dir:
    :return:
    """
    parent_dir = os.path.abspath(parent_dir)
    child_dir = os.path.abspath(child_dir)

    try:
        # 获取父目录和子目录的共同部分路径
        common_path = os.path.commonpath([parent_dir, child_dir])
        # 如果共同路径与父目录相同，说明子目录在父目录下
        return common_path == parent_dir
    except ValueError:
        return False


class HashUtil:
    @staticmethod
    def calculate_md5(text):
        """
        计算文本的 md5 哈希值
        :param text:
        :return:
        """
        md5 = hashlib.md5()
        md5.update(text.encode('utf-8'))
        return md5.hexdigest()


class BackupUtil:
    def __init__(self):
        pass

    @staticmethod
    def backup(source_path, target_path, filters=None):
        """
        :note: 暂时使用 shutil 库进行数据备份，存在无法知晓备份进度的问题，
        同时也无法暂停或停止备份，后续考虑重新实现备份功能
        :param source_path:
        :param target_path:
        :param filters:
        :return:
        """
        start_time = time.time()
        source_path = os.path.abspath(source_path)
        target_path = os.path.abspath(target_path)

        # 创建备份目录
        if os.path.isdir(target_path):
            os.makedirs(target_path, exist_ok=True)

        try:
            if os.path.isfile(source_path):
                print('backup file start')
                shutil.copy(source_path, target_path)
                print('backup file success')

            elif os.path.isdir(target_path):
                print('backup folder start')
                shutil.copytree(source_path, target_path,
                                ignore=shutil.ignore_patterns(*filters),
                                dirs_exist_ok=True)
                print('backup folder success')
            else:
                raise PathError("需要备份的源或目标目录错误，无法将文件夹备份至文件中")
        except IOError as _err:
            traceback.print_exc()
            raise BackupError("数据备份失败")

        finish_time = time.time()
        return finish_time - start_time


if __name__ == '__main__':
    # 调用函数进行文件夹备份
    source_path = r"D:\test_source_源"
    target_path = r"D:\test_target_目标"
    target_path = r"D:\test_target_目标\xxx.zip"

    BackupUtil.backup(source_path, target_path,
                      filters=[
                          # 'System Volume Information',
                          # '$360Section',
                          # '$RECYCLE.BIN',
                          # '$LBak',
                          # '$baksd',
                          # 'desktop.ini'
                          # 'hiberfil.sys',
                          # 'swapfile.sys',
                          # 'pagefile.sys',
                      ])
