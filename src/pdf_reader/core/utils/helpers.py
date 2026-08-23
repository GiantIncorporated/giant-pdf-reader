from pytestqt.qtbot import QWidget

import config

_STYLES_dir = config.PACKAGE_ROOT / "assets" / "styles"


def load_stylesheet(parent: QWidget, file: str):
    qss_path = _STYLES_dir / file
    try:
        parent.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        pass
