from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
    QTextEdit,
    QScrollArea,
)
from PySide6.QtGui import QFont
from ui_config import UiConfig
from env import NETWORK_DRIVE_USER, NETWORK_DRIVE_PASSWORD


class AboutSection(QWidget):
    def __init__(self):
        super(AboutSection, self).__init__()
        self.setup()

    def setup(self):
        self.main_layout = QVBoxLayout(self)

        self.main_scroll_area = QScrollArea(self)
        self.main_scroll_area.setWidgetResizable(True)

        self.contents = QWidget()
        self.contents_layout = QVBoxLayout(self.contents)

        self.title = QLabel(self.contents)
        self.title.setText("Acerca de")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setFamilies(UiConfig.FONT_FAMILY)
        self.title.setFont(title_font)

        self.text = QTextEdit(self.contents)
        self.text.setReadOnly(True)
        self.text.setPlainText(
            f"xd\nEl usuario para la carpeta compartida es: {NETWORK_DRIVE_USER}\nLa contraseña para la carpeta compartida es: {NETWORK_DRIVE_PASSWORD}\n\nLos precios de anillado son experimentales..... aun tengo que hacer la tabla de precios mejor o ponerlo como un campo editable"
        )
        text_font = QFont()
        text_font.setPointSize(12)
        text_font.setFamilies(UiConfig.FONT_FAMILY)
        self.text.setFont(text_font)

        self.contents_layout.addWidget(self.title)
        self.contents_layout.addWidget(self.text)

        self.main_scroll_area.setWidget(self.contents)
        self.main_layout.addWidget(self.main_scroll_area)

        self.setLayout(self.main_layout)
