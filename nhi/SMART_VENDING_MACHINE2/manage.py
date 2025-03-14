from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QTableWidget
from PyQt6 import uic
import sys

class ProductManager(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("manage.ui", self)

        self.table = self.findChild(QTableWidget, "tableWidget")  # Lấy bảng theo objectName
        self.table.setColumnCount(6)  # ID, Name, Category, Price, Quantity, Actions
        """Thêm dữ liệu """
        data = [
            (1, "Product 1", "Category A", "10.99", "5"),
            (2, "Product 2", "Category B", "15.99", "3"),
            (3, "Product 3", "Category C", "8.99", "7"),
        ]

        for row, (id, name, category, price, quantity) in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(price))
            self.table.setItem(row, 4, QTableWidgetItem(quantity))
            self.add_buttons(row)

    def add_buttons(self, row):
        """Thêm nút Edit và Delete vào bảng với màu sắc"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        """Nút Edit - Màu xanh lá """
        btn_edit = QPushButton("Edit")
        btn_edit.setFixedSize(80, 35)
        btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_edit.clicked.connect(lambda: self.edit_product(row))

        """Nút Delete - Màu đỏ """
        btn_delete = QPushButton("Delete")
        btn_delete.setFixedSize(80, 35)
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        btn_delete.clicked.connect(lambda: self.delete_product(row))

        """Thêm nút vào layout """
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        widget.setLayout(layout)

        """Đặt widget chứa nút vào bảng """
        self.table.setCellWidget(row, 5, widget)

    def edit_product(self, row):
        print(f"Chỉnh sửa sản phẩm ở dòng {row}")

    def delete_product(self, row):
        print(f"Xóa sản phẩm ở dòng {row}")
        self.table.removeRow(row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductManager()
    window.show()
    sys.exit(app.exec())
