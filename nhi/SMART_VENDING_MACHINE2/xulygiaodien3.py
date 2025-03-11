from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QLabel, QFrame, QPushButton, QGridLayout, QVBoxLayout, QTableWidgetItem
import sys
import json
from PyQt6.QtGui import QPixmap
from Product import Product
from Cart import Cart
from Function import *


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('giaodien.ui', self)
        self.functions = SmartMartFunctions()
        self.cart = self.functions.cart  # Sử dụng cart từ SmartMartFunctions
        self.product_frame = None
        self.selected_frame = None
        self.lienketnutlenh()
        self.setup_products()
        self.cart_table = self.findChild(QtWidgets.QTableWidget, "cart_table")  # Tham chiếu đến cart_table
        self.label_total = self.findChild(QtWidgets.QLabel, "label_total")  # Tham chiếu đến label_total
        self.search_bar = self.findChild(QtWidgets.QLineEdit, "search_bar")
        self.show()

    def lienketnutlenh(self):
        self.pushButton_SEARCH.clicked.connect(self.search_product)
        self.pushButton_ADD.clicked.connect(self.add_to_cart)
        self.pushButton_REMOVE.clicked.connect(self.remove_from_cart)
        self.pushButton_CHECKOUT.clicked.connect(self.checkout)
        # Kết nối các nút danh mục với filter_product
        self.pushButton_Beverages.clicked.connect(lambda: self.filter_product("Beverages"))
        self.pushButton_FastFood.clicked.connect(lambda: self.filter_product("Fast Food"))
        self.pushButton_Snacks.clicked.connect(lambda: self.filter_product("Snacks"))
        self.pushButton_PersonalCares.clicked.connect(lambda: self.filter_product("Personal Cares"))

    def setup_products(self):
        self.scroll_area = self.findChild(QtWidgets.QScrollArea, "scrollArea_products")
        self.scroll_content2 = self.findChild(QtWidgets.QWidget, "scrollContent2")
        self.product_container = self.findChild(QtWidgets.QGridLayout, "productContainer")

        self.product_container.setSpacing(10)  # Giãn cách sản phẩm

        self.load_products()

    def load_products(self):
        # Gọi hàm load_products từ SmartMartFunctions để tải dữ liệu
        self.functions.load_products()

        # Lấy dữ liệu sản phẩm từ SmartMartFunctions
        self.products = self.functions.products

        # Hiển thị danh mục mặc định (ví dụ: "Beverages")
        self.filter_product("Beverages")

    def add_product(self, row, col, name, price, image_path, stock, category):
        product_frame = QFrame()
        product_frame.setLayout(QVBoxLayout())

        # Tạo QLabel chứa ảnh
        label_image = QLabel()
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"⚠️ Lỗi: Không tìm thấy ảnh {image_path}")
        else:
            label_image.setPixmap(pixmap)
            label_image.setScaledContents(True)  # Để ảnh tự co giãn vừa khung

        # Tạo QPushButton chứa tên, giá và số lượng stock
        button_product = QPushButton(f"{name}\n{price}đ\nStock: {stock}")
        button_product.clicked.connect(lambda checked, frame=product_frame: self.hightlight(frame))

        # Lưu thông tin sản phẩm vào button_product
        button_product.product_name = name
        button_product.product_price = price
        button_product.product_stock = stock

        # Thêm vào layout của sản phẩm
        product_frame.layout().addWidget(label_image)
        product_frame.layout().addWidget(button_product)

        self.product_container.addWidget(product_frame, row, col)

    def update_cart_list(self):
        self.cart_table.setRowCount(0)  # Xóa tất cả các hàng hiện có
        for product_name, quantity in self.functions.cart.items.items():
            for category, products in self.functions.products.items():
                for product in products:
                    if product.name == product_name:
                        row_position = self.cart_table.rowCount()
                        self.cart_table.insertRow(row_position)
                        self.cart_table.setItem(row_position, 0, QTableWidgetItem(product_name))
                        self.cart_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))
                        self.cart_table.setItem(row_position, 2, QTableWidgetItem(str(product.price)))
                        break

    def search_product(self):
        search_text = self.search_bar.text().lower()
        # Xóa các widget cũ
        for i in reversed(range(self.product_container.count())):
            widget = self.product_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Hiển thị sản phẩm phù hợp với từ khóa tìm kiếm
        row, col = 0, 0
        for category, products in self.products.items():
            for product in products:
                if search_text in product["name"].lower():
                    self.add_product(row, col, product["name"], product["price"], product["image"], product["stock"])
                    col += 1
                    if col >= 3:  # 3 cột mỗi hàng
                        col = 0
                        row += 1

    def add_to_cart(self):
        if not hasattr(self, "selected_frames") or not self.selected_frames:
            QMessageBox.warning(self, "Error", "Vui lòng chọn ít nhất một sản phẩm trước.")

        for selected_frame in self.selected_frames:
            product_button = selected_frame.findChild(QPushButton)
            if product_button:
                product_name = product_button.product_name  # Lấy tên sản phẩm từ thuộc tính
                if self.functions.add_to_cart(product_name):
                    self.update_cart_list()
                else:
                    QMessageBox.warning(self, "Error", f"Không thể thêm {product_name} vào giỏ hàng.")

    def hightlight(self, selected_frame):
        if not hasattr(self, "selected_frames"):
            self.selected_frames = []

        if selected_frame in self.selected_frames:
            # Nếu frame đã được chọn, bỏ chọn nó
            self.selected_frames.remove(selected_frame)
            selected_frame.setStyleSheet("QFrame { border: none; }")
        else:
            # Nếu frame chưa được chọn, thêm vào danh sách chọn
            self.selected_frames.append(selected_frame)
            selected_frame.setStyleSheet("""
                QFrame {
                    border: 2px solid #ADD8E6;  /* Viền xanh nhạt */
                    border-radius: 4px;
                }
                QLabel, QPushButton {
                    border: none;  /* Đảm bảo QLabel và QPushButton không bị viền */
                    background: transparent;
                }
            """)

    def remove_from_cart(self):
        selected_row = self.cart_table.currentRow()  # Lấy hàng được chọn trong cart_table
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Vui lòng chọn một sản phẩm từ giỏ hàng.")
            return

        product_name = self.cart_table.item(selected_row, 0).text()  # Lấy tên sản phẩm từ hàng được chọn
        if self.functions.remove_from_cart(product_name):
            self.update_cart_list()  # Cập nhật lại bảng giỏ hàng
            category = self.functions.get_product_category(product_name)
            if category:
                self.filter_product(category)  # Cập nhật lại danh sách sản phẩm
        else:
            QMessageBox.warning(self, "Error", f"Không thể xóa {product_name} khỏi giỏ hàng.")

    def checkout(self):
        total = self.functions.checkout()
        if total == -1:
            QMessageBox.warning(self, "Error", "Your cart is empty.")
        else:
            # Hiển thị tổng tiền trong label_total
            self.label_total.setText(f"Total: {total:.2f}đ")

            # Thông báo thanh toán thành công
            QMessageBox.information(self, "Checkout",
                                    f"Total: {total:.2f}đ\nPayment successful! Dispensing your items.")

            # Cập nhật lại giỏ hàng và danh sách sản phẩm
            self.update_cart_list()

    def filter_product(self, category):
        if hasattr(self, "selected_frames"):
            self.selected_frames.clear()
        # Xóa các widget cũ
        for i in reversed(range(self.product_container.count())):
            widget = self.product_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Hiển thị sản phẩm trong danh mục được chọn
        if category in self.products:
            products = self.products[category]
            row, col = 0, 0
            for product in products:
                self.add_product(row, col, product["name"], product["price"], product["image"], product["stock"],
                                 category)
                col += 1
                if col >= 3:  # 3 cột mỗi hàng
                    col = 0
                    row += 1


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()
