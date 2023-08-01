import hashlib
import os
from pathlib import Path


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
