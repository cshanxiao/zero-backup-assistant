from pathlib import Path

import settings

font_path = Path(settings.RESOURCE_PATH).joinpath("fonts/SourceCodePro-LightIt.ttf").as_posix()
print(type(font_path), font_path)

font_path = Path(settings.RESOURCE_PATH).joinpath("fonts/SourceCodePro-LightIt.ttf").absolute()
print(type(font_path), font_path)
