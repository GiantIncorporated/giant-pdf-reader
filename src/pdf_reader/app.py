import sys

from PySide6.QtWidgets import QApplication
from pdf_reader.config import APP_NAME, ORG_NAME
from pdf_reader.ui.main_window import MainWindow


def create_app() -> QApplication:
    """Construct and configure the QApplication instance."""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORG_NAME)
    return app


def main() -> None:
    app = create_app()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # Allows `python -m myapp.app` as a fallback during development,
    # but __main__.py is the intended entry point.
    main()