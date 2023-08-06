# -*- coding: utf8 -*-
"""
@summary:
@author: Zero
@date: 2023年8月1日
"""

import cgitb
import sys
import traceback
from pathlib import Path

from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication

import settings
from backup.control.main_dlg import MainDialog
from backup.common.logger import logger

# 开发过程中捕捉全部异常
cgitb.enable(format='text')


def main():
    try:
        app = QApplication(sys.argv)
        # 设置字体
        font_path = Path(settings.RESOURCE_PATH) / "fonts/SourceCodePro-LightIt.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path.as_posix())
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont(font_families[0], 12)
        app.setFont(font)

        dlg = MainDialog()
        dlg.show()
        app.exec()
    except Exception as err:
        traceback.print_exc()
        logger.error(f"app excepted, err: {err}")


if __name__ == '__main__':
    main()
