import os
import shutil
import traceback

from backup.common.eception import PathError, BackupError


class BackupUtil:
    def __init__(self):
        pass

    @staticmethod
    def backup(source_path, target_path, filters=None):
        source_path = os.path.abspath(source_path)
        target_path = os.path.abspath(target_path)

        # 创建备份目录
        if os.path.isdir(target_path):
            os.makedirs(target_path, exist_ok=True)

        try:
            if os.path.isfile(source_path):
                print('backup file')
                shutil.copy(source_path, target_path)
                print('backup file success')

            elif os.path.isdir(target_path):
                print('backup folder')
                shutil.copytree(source_path, target_path,
                                ignore=shutil.ignore_patterns(*filters),
                                dirs_exist_ok=True)
                print('backup folder success')
            else:
                raise PathError("需要备份的源或目标目录错误，无法将文件夹备份至文件中")
        except IOError as _err:
            traceback.print_exc()
            raise BackupError("数据备份失败")


if __name__ == '__main__':
    # 调用函数进行文件夹备份
    source_path = r"D:\test_source_源"
    target_path = r"D:\test_target_目标"
    target_path = r"D:\test_target_目标1\xxx.zip"

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
                      ]
                      )
