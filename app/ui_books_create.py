import os
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QMessageBox,
    QFrame,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from ui_config import UiConfig
from fn_api import FnStore, api_create_book, api_create_category


class BooksCreate(QWidget):
    def __init__(self):
        super(BooksCreate, self).__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("Crear libro")
        self.main_layout = QVBoxLayout(self)

        inputs_font = QFont()
        inputs_font.setFamilies(UiConfig.FONT_FAMILY)
        inputs_font.setPointSize(10)

        self.title = QLabel(self, text="Crear libro")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)        
        title_font = QFont()
        title_font.setFamilies(UiConfig.FONT_FAMILY)
        title_font.setPointSize(16)
        self.title.setFont(title_font)
        self.main_layout.addWidget(self.title)

        subtitle_font = QFont()
        subtitle_font.setFamilies(UiConfig.FONT_FAMILY)
        subtitle_font.setPointSize(14)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(line)

        self.file_subtitle = QLabel(self, text="Archivo")
        self.file_subtitle.setFont(subtitle_font)
        self.main_layout.addWidget(self.file_subtitle)

        self.file_input = QPushButton(self, text="Seleccionar archivo")
        self.file_input.clicked.connect(self.select_file)
        self.main_layout.addWidget(self.file_input)

        self.file_description = QLabel(self, text="Archivo no seleccionado")
        self.file_description.setFont(inputs_font)
        self.file_description.setVisible(False)
        self.main_layout.addWidget(self.file_description)

        self.file_tip = QLabel(self, text="Las palabras del nombre del archivo deben estar separadas por espacios")
        file_tip_font = QFont()
        file_tip_font.setFamilies(UiConfig.FONT_FAMILY)
        file_tip_font.setPointSize(8)
        self.file_tip.setFont(file_tip_font)
        self.main_layout.addWidget(self.file_tip)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(line)

        self.category_subtitle = QLabel(self, text="Categoría")
        self.category_subtitle.setFont(subtitle_font)
        self.main_layout.addWidget(self.category_subtitle)

        self.category_combo = QComboBox(self)
        self.category_combo.setFont(inputs_font)
        self.category_combo.addItems(FnStore.CATEGORY_CHOICES)
        self.category_combo.addItem("Otro")
        self.category_combo.currentIndexChanged.connect(self.category_changed)
        self.main_layout.addWidget(self.category_combo)

        self.other_category_edit = QLineEdit(self)
        self.other_category_edit.setPlaceholderText("Otra categoría")
        self.other_category_edit.setFont(inputs_font)
        self.other_category_edit.setVisible(False)
        self.main_layout.addWidget(self.other_category_edit)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(line)

        self.bounded_price_subtitle = QLabel(self, text="Precio Empastado")
        self.bounded_price_subtitle.setFont(subtitle_font)
        self.main_layout.addWidget(self.bounded_price_subtitle)

        self.bounded_price_edit = QDoubleSpinBox(self)
        self.bounded_price_edit.setPrefix("S/. ")
        self.bounded_price_edit.setDecimals(2)
        self.main_layout.addWidget(self.bounded_price_edit)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(line)

        self.save_button = QPushButton(self)
        self.save_button.setText("Guardar")
        self.save_button.clicked.connect(self.create_book)
        self.main_layout.addWidget(self.save_button)

    def category_changed(self):
        self.other_category_edit.setVisible(
            self.category_combo.currentIndex() == len(FnStore.CATEGORY_CHOICES)
        )

    def create_book(self):
        response = QMessageBox.question(
            self,
            "Confirmar",
            "¿Está seguro de que desea crear el libro?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if response == QMessageBox.StandardButton.No:
            return

        if self.category_combo.currentIndex() == len(FnStore.CATEGORY_CHOICES):
            category_name = self.other_category_edit.text()
            category_id = api_create_category(category_name)
        else:
            category_id = self.category_combo.currentIndex() + 1
        if api_create_book(self.chosen_file, self.bounded_price_edit.value(), category_id):
            QMessageBox.information(self, "Libro creado", "El libro ha sido creado")
        else:
            QMessageBox.critical(self, "Error", "Hubo un error al crear el libro")

    def select_file(self):
        self.chosen_file, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo", "", "PDF (*.pdf)"
        )
        self.file_description.setVisible(True)
        self.file_description.setText(os.path.basename(self.chosen_file).split(".")[0])
        self.file_tip.setVisible(False)
