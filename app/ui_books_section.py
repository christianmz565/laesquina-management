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
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from fn_api import (
    api_download_book,
    api_search_books,
    api_update_book,
    FnStore,
)
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
        self.results_table.setColumnCount(5)

        id_header = QTableWidgetItem()
        id_header.setText("ID")
        self.results_table.setHorizontalHeaderItem(0, id_header)
        name_header = QTableWidgetItem()
        name_header.setText("Nombre")
        self.results_table.setHorizontalHeaderItem(1, name_header)
        category_header = QTableWidgetItem()
        category_header.setText("Categoria")
        self.results_table.setHorizontalHeaderItem(2, category_header)
        price_header = QTableWidgetItem()
        price_header.setText("Precio")
        self.results_table.setHorizontalHeaderItem(3, price_header)
        actions_header = QTableWidgetItem()
        actions_header.setText("Acciones")
        self.results_table.setHorizontalHeaderItem(4, actions_header)

        self.results_table.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

        # TODO: disabled until it stops causing bugs :<
        # self.results_table.setSortingEnabled(True)

        self.results_table.horizontalHeader().setMinimumSectionSize(50)
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

        name_item = QTableWidgetItem()
        name_item.setText(book.name)
        self.results_table.setItem(row, 1, name_item)

        category_item = QTableWidgetItem()
        category_item.setText(FnStore.CATEGORIES[book.category_id])
        self.results_table.setItem(row, 2, category_item)
        self.results_table.cellDoubleClicked.connect(
            lambda r, c: self.change_category_to_combobox(r, c, row, book.category_id)
        )

        price_item = QTableWidgetItem()
        price_item.setData(
            Qt.ItemDataRole.DisplayRole, (0.0 if book.price is None else book.price)
        )
        self.results_table.setItem(row, 3, price_item)

        download_item = QWidget()
        download_item_layout = QHBoxLayout(download_item)
        download_item.setLayout(download_item_layout)

        open_button = QPushButton(download_item)
        open_button.setText("Abrir")
        open_button.clicked.connect(lambda: self.download_book(book.id))
        download_item_layout.addWidget(open_button)

        update_button = QPushButton(download_item)
        update_button.setText("Actualizar")
        update_button.clicked.connect(lambda: self.update_book(row))
        download_item_layout.addWidget(update_button)
        self.results_table.setCellWidget(row, 4, download_item)

    def change_category_to_combobox(self, row, column, current_row, current_id):
        if column == 2 and row == current_row:
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
        book_name = self.results_table.item(row, 1).data(Qt.ItemDataRole.DisplayRole)
        book_category_widget = self.results_table.cellWidget(row, 2)
        book_category = (
            book_category_widget.currentIndex() + 1
            if isinstance(book_category_widget, QComboBox)
            else None
        )
        book_price = self.results_table.item(row, 3).data(Qt.ItemDataRole.DisplayRole)

        if api_update_book(book_id, book_name, book_category, book_price):
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
