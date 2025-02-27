from PySide6.QtWidgets import QApplication
from ui_main import MainWindow
import sys
from fn_api import FnStore


if __name__ == "__main__":
    FnStore.load_categories()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
