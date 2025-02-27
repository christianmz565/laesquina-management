from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QMainWindow,
)
from ui_config import UiConfig
from ui_books_section import BooksSection
from ui_about_section import AboutSection


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("La Esquina")
        self.resize(1000, 800)
        main_font = QFont()
        main_font.setFamilies(UiConfig.FONT_FAMILY)
        self.setFont(main_font)

        self.main_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.title = QLabel(self.main_widget)
        self.title.setText("La Esquina")
        title_font = QFont()
        title_font.setFamilies(UiConfig.FONT_FAMILY)
        title_font.setPointSize(26)
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title)

        self.main_tab_widget = QTabWidget(self.main_widget)
        self.main_tab_widget.setTabPosition(QTabWidget.TabPosition.West)

        self.books_section = BooksSection()

        self.main_tab_widget.addTab(self.books_section, "Libros")

        self.about_section = AboutSection()

        self.main_tab_widget.addTab(self.about_section, "Acerca de")

        self.main_layout.addWidget(self.main_tab_widget)
        self.setCentralWidget(self.main_widget)
