from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QLineEdit,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QMessageBox,
)
import math
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from fn_api import (
    api_download_book,
    api_search_books,
    api_update_book,
)
from fn_config import FnConfig
from fn_api import FnStore
from models import Book
from ui_books_create import BooksCreate
from ui_config import UiConfig


class BooksSection(QWidget):
    def __init__(self):
        super(BooksSection, self).__init__()
        self.setup()

    def setup(self):
        self.main_layout = QVBoxLayout(self)

        self.main_scroll_area = QScrollArea(self)
        self.main_scroll_area.setWidgetResizable(True)

        self.contents = QWidget()
        self.contents_layout = QVBoxLayout(self.contents)

        self.top_bar = QWidget(self.contents)
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        top_bar_font = QFont()
        top_bar_font.setFamilies(UiConfig.FONT_FAMILY)
        top_bar_font.setPointSize(14)

        self.search_edit = QLineEdit(self.contents)
        self.search_edit.setFont(top_bar_font)
        self.search_edit.returnPressed.connect(self.search_books)
        self.top_bar_layout.addWidget(self.search_edit)

        self.add_button = QPushButton(self.contents)
        self.add_button.setFont(top_bar_font)
        self.add_button.setText("Crear")
        self.add_button.clicked.connect(self.create_book)
        self.top_bar_layout.addWidget(self.add_button)

        self.contents_layout.addWidget(self.top_bar)

        self.results_table = QTableWidget(self.contents)
        self.results_table.setColumnCount(11)

        id_header = QTableWidgetItem()
        id_header.setText("ID")
        self.results_table.setHorizontalHeaderItem(0, id_header)
        open_header = QTableWidgetItem()
        open_header.setText("Abrir")
        self.results_table.setHorizontalHeaderItem(1, open_header)
        name_header = QTableWidgetItem()
        name_header.setText("Nombre")
        self.results_table.setHorizontalHeaderItem(2, name_header)
        category_header = QTableWidgetItem()
        category_header.setText("Categoria")
        self.results_table.setHorizontalHeaderItem(3, category_header)
        bounded_header = QTableWidgetItem()
        bounded_header.setText("Empastado")
        self.results_table.setHorizontalHeaderItem(4, bounded_header)
        bn_a5_header = QTableWidgetItem()
        bn_a5_header.setText("B/N A5")
        self.results_table.setHorizontalHeaderItem(5, bn_a5_header)
        bn_a4_header = QTableWidgetItem()
        bn_a4_header.setText("B/N A4")
        self.results_table.setHorizontalHeaderItem(6, bn_a4_header)
        color_a5_header = QTableWidgetItem()
        color_a5_header.setText("Color A5")
        self.results_table.setHorizontalHeaderItem(7, color_a5_header)
        color_a4_header = QTableWidgetItem()
        color_a4_header.setText("Color A4")
        self.results_table.setHorizontalHeaderItem(8, color_a4_header)
        spiral_header = QTableWidgetItem()
        spiral_header.setText("Anillado")
        self.results_table.setHorizontalHeaderItem(9, spiral_header)
        update_header = QTableWidgetItem()
        update_header.setText("Actualizar")
        self.results_table.setHorizontalHeaderItem(10, update_header)

        self.results_table.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

        # TODO: disabled until it stops causing bugs :<
        # self.results_table.setSortingEnabled(True)

        self.results_table.horizontalHeader().setMinimumSectionSize(60)
        self.results_table.horizontalHeader().setDefaultSectionSize(160)
        self.results_table.horizontalHeader().setProperty("showSortIndicator", True)
        self.results_table.verticalHeader().setVisible(False)

        self.contents_layout.addWidget(self.results_table)
        self.main_scroll_area.setWidget(self.contents)
        self.main_layout.addWidget(self.main_scroll_area)
        self.setLayout(self.main_layout)

    def add_results_items(self, books: list[Book]):
        for book in books:
            self.add_results_item(book)
        self.results_table.resizeColumnsToContents()
        self.results_table.resizeRowsToContents()

    def clear_results(self):
        self.results_table.setRowCount(0)

    def add_results_item(self, book: Book):
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)

        id_item = QTableWidgetItem()
        id_item.setData(Qt.ItemDataRole.DisplayRole, book.id)
        id_item.setFlags(Qt.ItemFlag.ItemIsEditable)
        self.results_table.setItem(row, 0, id_item)

        open_item = QPushButton()
        open_item.setText("Abrir")
        open_item.clicked.connect(lambda: self.download_book(book.id))
        self.results_table.setCellWidget(row, 1, open_item)

        name_item = QTableWidgetItem()
        name_item.setText(book.name)
        self.results_table.setItem(row, 2, name_item)

        category_item = QTableWidgetItem()
        category_item.setText(FnStore.CATEGORIES[book.category_id])
        self.results_table.setItem(row, 3, category_item)
        self.results_table.cellDoubleClicked.connect(
            lambda r, c: self.change_category_to_combobox(r, c, row, book.category_id)
        )

        bounded_item = QTableWidgetItem()
        bounded_item.setData(
            Qt.ItemDataRole.DisplayRole, book.bounded_price if book.bounded_price else 0
        )
        self.results_table.setItem(row, 4, bounded_item)

        bn_a5_price = f"S/.{math.ceil(book.page_count * 0.025)}"
        bn_a5_item = QTableWidgetItem()
        bn_a5_item.setFlags(Qt.ItemFlag.ItemIsEditable)
        bn_a5_item.setData(Qt.ItemDataRole.DisplayRole, bn_a5_price)
        self.results_table.setItem(row, 5, bn_a5_item)

        bn_a4_price = f"S/.{math.ceil(book.page_count * 0.05)}"
        bn_a4_item = QTableWidgetItem()
        bn_a4_item.setFlags(Qt.ItemFlag.ItemIsEditable)
        bn_a4_item.setData(Qt.ItemDataRole.DisplayRole, bn_a4_price)
        self.results_table.setItem(row, 6, bn_a4_item)

        color_a5_price = f"S/.{math.ceil(book.page_count * 0.075)}"
        color_a5_item = QTableWidgetItem()
        color_a5_item.setFlags(Qt.ItemFlag.ItemIsEditable)
        color_a5_item.setData(Qt.ItemDataRole.DisplayRole, color_a5_price)
        self.results_table.setItem(row, 7, color_a5_item)

        color_a4_price = f"S/.{math.ceil(book.page_count * 0.15)}"
        color_a4_item = QTableWidgetItem()
        color_a4_item.setFlags(Qt.ItemFlag.ItemIsEditable)
        color_a4_item.setData(Qt.ItemDataRole.DisplayRole, color_a4_price)
        self.results_table.setItem(row, 8, color_a4_item)

        spiral_price = f"+{self.get_spiral_price_from_page_count(book.page_count)}"
        spiral_item = QTableWidgetItem()
        spiral_item.setFlags(Qt.ItemFlag.ItemIsEditable)
        spiral_item.setData(Qt.ItemDataRole.DisplayRole, spiral_price)
        self.results_table.setItem(row, 9, spiral_item)

        update_item = QPushButton()
        update_item.setText("Actualizar")
        update_item.clicked.connect(lambda: self.update_book(row))
        self.results_table.setCellWidget(row, 10, update_item)

    def get_spiral_price_from_page_count(self, page_count):
        for limit, price in FnConfig.SPIRAL_PRICE_UL:
            if page_count < limit:
                return price
        return -1

    def change_category_to_combobox(self, row, column, current_row, current_id):
        if column == 3 and row == current_row:
            category_item = QComboBox()
            category_item.addItems(FnStore.CATEGORY_CHOICES)
            category_item.setCurrentText(FnStore.CATEGORIES[current_id])
            self.results_table.setCellWidget(row, 2, category_item)

    def create_book(self):
        self.create_window = BooksCreate()
        self.create_window.show()

    def search_books(self):
        query_name = self.search_edit.text()
        books = api_search_books(name=query_name)
        self.clear_results()
        self.add_results_items(books)

    def download_book(self, book_id):
        api_download_book(book_id)

    def update_book(self, row):
        response = QMessageBox.question(
            self,
            "Actualizar libro",
            "¿Estás seguro de que deseas actualizar este libro?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if response == QMessageBox.StandardButton.No:
            return

        book_id = self.results_table.item(row, 0).data(Qt.ItemDataRole.DisplayRole)
        book_name = self.results_table.item(row, 2).data(Qt.ItemDataRole.DisplayRole)
        book_category_widget = self.results_table.cellWidget(row, 3)
        book_category = (
            book_category_widget.currentIndex() + 1
            if isinstance(book_category_widget, QComboBox)
            else None
        )
        book_bounded_price = self.results_table.item(row, 4).data(
            Qt.ItemDataRole.DisplayRole
        )

        if api_update_book(book_id, book_name, book_category, book_bounded_price):
            QMessageBox.information(
                self,
                "Actualización exitosa",
                "El libro se actualizó correctamente.",
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Increiblemente, algo salió mal al actualizar el libro.",
            )
