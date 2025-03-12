from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QLabel, QFrame, QPushButton, QVBoxLayout, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys
  # Import class quản lý sản phẩm và giỏ hàng
from CInvoice import Invoice
from CProductList import ProductList
from Cart import Cart


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('giaodien2.ui', self)
        # Khởi tạo các biến và tham chiếu UI
        # self.functions = SmartMartFunctions()  # Class quản lý sản phẩm và giỏ hàng
        self.productlist = ProductList()
        self.cart = Cart()
        self.selected_frames = []  # Danh sách các sản phẩm được chọn
        self.cart_table = self.findChild(QtWidgets.QTableWidget, "cart_table")
        self.label_total = self.findChild(QtWidgets.QLabel, "label_total")
        self.search_bar = self.findChild(QtWidgets.QLineEdit, "search_bar")
        self.scroll_area = self.findChild(QtWidgets.QScrollArea, "scrollArea_products")
        self.scrollContent2 = self.scroll_area.widget()  # Lấy widget chứa sản phẩm
        self.product_container = self.scrollContent2.findChild(QtWidgets.QGridLayout, "productContainer")
        self.scroll_area.setWidgetResizable(True)  # Đảm bảo có thể cuộn
        # self.scroll_content2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollContent2.adjustSize()

        self.scroll_area.widget().adjustSize()
        self.current_category = "Beverages"
        self.lienketnutlenh()
        self.setup_products()
        self.show()


    def lienketnutlenh(self):
        # Kết nối các nút với hàm xử lý
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
        # Thiết lập giao diện sản phẩm ban đầu
        # Thiết lập giao diện sản phẩm ban đầu
        self.scroll_widget = QtWidgets.QWidget()  # Widget chứa danh sách sản phẩm

        self.product_container = QtWidgets.QGridLayout(self.scroll_widget) # Sử dụng layout dọc thay vì grid
        self.product_container.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_widget)  # Đặt widget cuộn
        self.scroll_area.setWidgetResizable(True)
        self.load_products()

    def get_unique_categories(self):
        """Lấy danh sách danh mục không trùng lặp từ danh sách sản phẩm"""
        return sorted(set(product.category for product in self.productlist.products))

    def load_products(self):
        # Lấy danh sách sản phẩm từ SmartMartFunctions
        self.products = self.productlist.products

        # Hiển thị danh mục mặc định (ví dụ: "Beverages")
        self.filter_product("Beverages")

    def add_product(self, product, row, col):
        """Thêm sản phẩm vào lưới hiển thị"""
        product_frame = QFrame()
        product_frame.setLayout(QVBoxLayout())
        product_frame.setFixedSize(200, 241)

        # Hiển thị ảnh sản phẩm
        label_image = QLabel()
        pixmap = QPixmap(product.image)
        if not pixmap.isNull():

            label_image.setPixmap(pixmap)
        else:
            label_image.setText("No Image")
        label_image.setScaledContents(True)

        # Hiển thị thông tin sản phẩm
        button = QPushButton(f"{product.name}\nPrice: {product.price:,}đ | Stock: {product.stock}")
        button.clicked.connect(lambda checked, frame=product_frame: self.hightlight(frame))
        button.product_data = product
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #AFE1AF;
                color: black;
                font-size: 14px;
                border-radius: 6px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                border: 1px solid #4CAF50;
                color: #388E3C;
            }
            QPushButton:pressed {
                border: 2px solid #1B5E20;
                color: #1B5E20;
            }
        """)

        # Thêm vào layout
        product_frame.layout().addWidget(label_image)
        product_frame.layout().addWidget(button)

        # Thêm vào `QGridLayout` theo hàng và cột
        self.product_container.addWidget(product_frame, row, col)

    def add_to_cart(self):
        # Lấy sản phẩm được chọn từ danh sách highlight
        if not self.selected_frames:
            QMessageBox.warning(self, "Error", "Vui lòng chọn một sản phẩm để thêm vào giỏ hàng.")
            return

        # Duyệt qua từng frame sản phẩm được chọn
        for selected_frame in self.selected_frames:
            button = selected_frame.findChild(QPushButton)
            if button and hasattr(button, "product_data"):
                product = button.product_data  # Lấy đối tượng sản phẩm từ nút
                # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
                if not self.cart.add_product(product.id):
                    QMessageBox.warning(self, "Lỗi",
                                        f"Không thể thêm sản phẩm '{product.name}' vào giỏ hàng. Có thể số lượng tồn kho không đủ.")
                # if self.cart.has_item(product.id):  # Nếu đã có trong giỏ hàng

        # Cập nhật lại bảng giỏ hàng sau khi xử lý tất cả sản phẩm
        self.update_cart_table()

        # Xóa danh sách sản phẩm được chọn sau khi thêm vào giỏ hàng
        self.selected_frames.clear()
        # Làm mới lại danh sách sản phẩm để cập nhật stock
        self.filter_product(self.current_category)

    def update_cart_table(self):
        self.cart_table.setRowCount(0) # Xóa tất cả các dòng hiện tại
        self.label_total.clear()
        for row, item in enumerate(self.cart.to_dict()):  # Duyệt qua từng mục trong giỏ hàng
            product = self.productlist.get_product_by_id(item['product_id'])  # Tìm sản phẩm bằng product_id
            if product:
                self.cart_table.insertRow(row)
                # Tên sản phẩm
                self.cart_table.setItem(row, 0, QTableWidgetItem(product.name))
                # Số lượng
                self.cart_table.setItem(row, 1, QTableWidgetItem(str(item['qty'])))  # Chuyển số lượng thành chuỗi
                # Giá
                self.cart_table.setItem(row, 2, QTableWidgetItem(f"{product.price:,}đ"))
        self.cart_table.verticalHeader().setVisible(False)

    def search_product(self):
        # Tìm kiếm sản phẩm theo từ khóa
        search_text = self.search_bar.text().lower()

        # Xóa các widget cũ
        for i in reversed(range(self.product_container.count())):
            widget = self.product_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Hiển thị sản phẩm phù hợp với từ khóa tìm kiếm
        row, col = 0, 0
        for product in self.productlist.products:
            if search_text in product.name.lower():
                self.add_product(product, row, col)
                col += 1
                if col >= 3:  # 3 cột mỗi hàng
                    col = 0
                    row += 1

    def hightlight(self, selected_frame):
        # Highlight sản phẩm khi được chọn
        if selected_frame in self.selected_frames:
            # Nếu frame đã được chọn, bỏ chọn nó
            self.selected_frames.remove(selected_frame)
            selected_frame.setStyleSheet("QFrame { border: none; }")
        else:
            # Nếu frame chưa được chọn, thêm vào danh sách chọn
            self.selected_frames.append(selected_frame)
            selected_frame.setStyleSheet("""
                            QFrame {
                                border: 2px solid #A3D9A5;  /* Viền xanh nhạt */
                                border-radius: 6px;
                            }
                            QLabel, QPushButton {
                                border: none;  /* Đảm bảo QLabel và QPushButton không bị viền */
                                background: transparent;
                            }
                        """)

    def remove_from_cart(self):
        """
        Xóa sản phẩm khỏi giỏ hàng dựa trên thông tin hiển thị trong bảng.
        Không cần lấy product_id, sử dụng tên sản phẩm để xác định.
        """
        # Kiểm tra xem giỏ hàng có trống không
        if self.cart_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "Giỏ hàng đang trống.")
            return

        # Lấy dòng được chọn trong bảng giỏ hàng
        selected_row = self.cart_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Vui lòng chọn một sản phẩm trong giỏ hàng.")
            return

        # Lấy tên sản phẩm từ cột đầu tiên (cột tên sản phẩm)
        product_name_item = self.cart_table.item(selected_row, 0)
        if not product_name_item:
            QMessageBox.warning(self, "Error", "Không thể xác định sản phẩm được chọn.")
            return

        product_name = product_name_item.text()  # Lấy tên sản phẩm

        # Tìm sản phẩm trong giỏ hàng dựa trên tên
        product_to_remove = None
        for item in self.cart.to_dict():
            product = self.productlist.get_product_by_id(item['product_id'])
            if product and product.name == product_name:
                product_to_remove = product
                break

        if not product_to_remove:
            QMessageBox.warning(self, "Error", "Không tìm thấy sản phẩm trong giỏ hàng.")
            return

        # Xóa sản phẩm khỏi giỏ hàng
        self.cart.remove_product(product_to_remove.id)
        self.update_cart_table()  # Cập nhật lại bảng giỏ hàng
        QMessageBox.information(self, "Success", f"Sản phẩm '{product_name}' đã được xóa khỏi giỏ hàng.")

    def checkout(self):
        total, tax, total_after_tax = self.cart.checkout()

        if total == -1:
            QMessageBox.warning(self, "Error", "Giỏ hàng đang trống.")
        else:
            invoice = Invoice(self.cart.get_cart(), total,tax, total_after_tax)  # Tạo hóa đơn mới

            invoice.save_to_json()  # Lưu vào file JSON
            invoice.generate_invoice()

            for item in self.cart.to_dict():
                success = self.productlist.reduce_stock(item['product_id'], item['qty'])
                if success is False:
                    QMessageBox.warning(self, "Lỗi", f"Sản phẩm {item['product_id']} không đủ hàng.")

            self.productlist.load_products()
            self.load_products()
            self.cart.clear()
            self.label_total.setText(f" {invoice.total:,.0f}đ")
            QMessageBox.information(self, "Checkout", f"Tổng tiền: {invoice.total:.0f}đ\n Tien thue: {invoice.tax:.0f}\n Tong tien sau thue: {invoice.total_after_tax:.0f} \nThanh toán thành công!")

            self.update_cart_table()  # Cập nhật lại giao diện giỏ hàng

    def filter_product(self, category="Beverages"):
        # Cập nhật danh mục hiện tại
        self.current_category = category

        if hasattr(self, "selected_frames"):
            self.selected_frames.clear()

        # Lọc sản phẩm theo danh mục
        filtered_products = [p for p in self.productlist.products if p.category == category]

        # Xóa widget cũ
        for i in reversed(range(self.product_container.count())):
            widget = self.product_container.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Thêm sản phẩm vào layout theo hàng và cột
        row, col = 0, 0
        for product in filtered_products:
            self.add_product(product, row, col)
            col += 1
            if col >= 3:  # Hiển thị 3 sản phẩm trên một hàng
                col = 0
                row += 1

        self.scroll_widget.adjustSize()  # Điều chỉnh kích thước widget cuộn
        self.scroll_area.verticalScrollBar().setValue


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()
