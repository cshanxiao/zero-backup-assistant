"""
Core exceptions raised by the application
"""


class AppError(Exception):
    pass


class PathError(AppError):
    """
    文件路径错误
    """
    pass


class BackupError(AppError):
    """
    备份错误
    """
    pass
