# -*- coding: utf8 -*-
u"""
@summary:
@author: Zero
@date: 2016年2月18日
"""

import cgitb
import sys
import traceback
from pathlib import Path

from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication

import settings
from backup.control.main_dlg import MainDialog

# 开发过程中捕捉全部异常
cgitb.enable(format='text')


def main():
    try:
        app = QApplication(sys.argv)
        # 设置字体
        font_path = Path(settings.RESOURCE_PATH).joinpath("fonts/SourceCodePro-LightIt.ttf").as_posix()
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        font_name = font_families[0]
        font = QFont(font_name, 12)
        app.setFont(font)

        dlg = MainDialog()
        dlg.show()
        app.exec()
    except:
        traceback.print_exc()


if __name__ == '__main__':
    main()
