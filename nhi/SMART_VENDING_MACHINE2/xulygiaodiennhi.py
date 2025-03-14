
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QLabel, QFrame, QPushButton, QVBoxLayout, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
import sys
from CInvoice import Invoice
from CProductList import ProductList
from Cart import Cart
from CAdmin_list import *
from InvoiceDialog import InvoiceDialog
from nhi.SMART_VENDING_MACHINE2.test import admin_name


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('giaodien2.ui', self)
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
        self.scrollContent2.adjustSize()
        self.pushButton_icon = self.findChild(QtWidgets.QPushButton, "pushButton_icon")

        icon = QIcon("image/icon.jpg")
        self.pushButton_icon.setIcon(icon)
        self.pushButton_icon.setIconSize(QSize(30, 30))

        self.scroll_area.widget().adjustSize()
        self.current_category = "Beverages"
        self.lienketnutlenh()
        self.setup_products()
        self.show()


    def lienketnutlenh(self):
        """Kết nối nút lệnh với hàm"""
        self.pushButton_SEARCH.clicked.connect(self.search_product)
        self.pushButton_ADD.clicked.connect(self.add_to_cart)
        self.pushButton_REMOVE.clicked.connect(self.remove_from_cart)
        self.pushButton_CHECKOUT.clicked.connect(self.checkout)
        self.pushButton_icon.clicked.connect(self.open_login_window)
        self.pushButton_ADD_2.clicked.connect(self.cancle)
        self.pushButton_icon.clicked.connect(self.open_login_window)

        """Kết nối các nút danh mục với filter_product"""
        self.pushButton_Beverages.clicked.connect(lambda: self.filter_product("Beverages"))
        self.pushButton_FastFood.clicked.connect(lambda: self.filter_product("Fast Food"))
        self.pushButton_Snacks.clicked.connect(lambda: self.filter_product("Snacks"))
        self.pushButton_PersonalCares.clicked.connect(lambda: self.filter_product("Personal Cares"))

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()


    def setup_products(self):
        """ Thiết lập giao diện sản phẩm ban đầu"""
        self.scroll_widget = QtWidgets.QWidget()

        self.product_container = QtWidgets.QGridLayout(self.scroll_widget)
        self.product_container.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.load_products()

    def get_unique_categories(self):
        """Lấy danh sách danh mục không trùng lặp từ danh sách sản phẩm"""
        return sorted(set(product.category for product in self.productlist.products))

    def load_products(self):
        """Lấy danh sách sản phẩm từ SmartMartFunctions"""
        self.products = self.productlist.products

        """ Hiển thị danh mục mặc định"""
        self.filter_product("Beverages")

    def add_product(self, product, row, col):
        """Thêm sản phẩm vào lưới hiển thị"""
        product_frame = QFrame()
        product_frame.setLayout(QVBoxLayout())
        product_frame.setFixedSize(200, 241)

        """Hiển thị ảnh sản phẩm"""
        label_image = QLabel()
        pixmap = QPixmap(product.image)
        if not pixmap.isNull():

            label_image.setPixmap(pixmap)
        else:
            label_image.setText("No Image")
        label_image.setScaledContents(True)

        """ Hiển thị thông tin sản phẩm"""
        button = QPushButton(f"{product.name}\nPrice: {product.price:,}đ | Stock: {product.stock}")
        button.clicked.connect(lambda checked, frame=product_frame: self.hightlight(frame))
        button.product_data = product
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #AFE1AF;
                color: black;
                font-size: 12px;
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

        """ Thêm vào layout"""
        product_frame.layout().addWidget(label_image)
        product_frame.layout().addWidget(button)

        """ Thêm hàng và cột"""
        self.product_container.addWidget(product_frame, row, col)

    def add_to_cart(self):
        """ Lấy sản phẩm được chọn từ danh sách highlight"""
        if not self.selected_frames:
            QMessageBox.warning(self, "Error", "Vui lòng chọn một sản phẩm để thêm vào giỏ hàng.")
            return

        """ Duyệt qua từng frame sản phẩm được chọn"""
        for selected_frame in self.selected_frames:
            button = selected_frame.findChild(QPushButton)
            if button and hasattr(button, "product_data"):
                product = button.product_data
                """ Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa"""
                if not self.cart.add_product(product.id):
                    QMessageBox.warning(self, "Lỗi",
                                        f"Không thể thêm sản phẩm '{product.name}' vào giỏ hàng. Có thể số lượng tồn kho không đủ.")

        """ Cập nhật lại bảng giỏ hàng sau khi xử lý tất cả sản phẩm"""
        self.update_cart_table()

        """ Xóa danh sách sản phẩm được chọn sau khi thêm vào giỏ hàng"""
        self.selected_frames.clear()
        self.update_total_price()
        """ Làm mới lại danh sách sản phẩm để cập nhật stock"""
        self.filter_product(self.current_category)

    def update_total_price(self):
        sub_total, tax, total  = self.cart.get_total()  # Chỉ lấy tổng tiền, bỏ qua thuế
        self.label_subtotal.setText(f"{sub_total:,.0f}đ")
        self.label_tax.setText(f"{tax:,.0f}đ")
        self.label_total.setText(f"{total:,.0f}đ")# Cập nhật giao diện


    def update_cart_table(self):
        self.cart_table.setRowCount(0) # Xóa tất cả các dòng hiện tại
        self.label_subtotal.clear()
        self.label_total.clear()
        self.label_tax.clear()
        for row, item in enumerate(self.cart.to_dict()):  # Duyệt qua từng mục trong giỏ hàng
            product = self.productlist.get_product_by_id(item['product_id'])
            if product:
                self.cart_table.insertRow(row)
                """ Tên sản phẩm"""
                self.cart_table.setItem(row, 0, QTableWidgetItem(product.name))
                """ Số lượng"""
                self.cart_table.setItem(row, 1, QTableWidgetItem(str(item['qty'])))
                product_total = item['qty'] * product.price
                """ Giá"""
                self.cart_table.setItem(row, 2, QTableWidgetItem(f"{product_total:,.0f}đ"))
        self.cart_table.verticalHeader().setVisible(False)

    def search_product(self):
        """ Tìm kiếm sản phẩm theo từ khóa"""
        search_text = self.search_bar.text().lower()

        """ Xóa các widget cũ"""
        for i in reversed(range(self.product_container.count())):
            widget = self.product_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        """ Hiển thị sản phẩm phù hợp với từ khóa tìm kiếm"""
        row, col = 0, 0
        for product in self.productlist.products:
            if search_text in product.name.lower():
                self.add_product(product, row, col)
                col += 1
                if col >= 3:  # 3 cột mỗi hàng
                    col = 0
                    row += 1

    def hightlight(self, selected_frame):
        """ Highlight sản phẩm khi được chọn"""
        if selected_frame in self.selected_frames:
            """ Nếu frame đã được chọn, bỏ chọn nó"""
            self.selected_frames.remove(selected_frame)
            selected_frame.setStyleSheet("QFrame { border: none; }")
        else:
            """ Nếu frame chưa được chọn, thêm vào danh sách chọn"""
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
        """Xóa sản phẩm khỏi giỏ hàng dựa trên thông tin hiển thị trong bảng.
        Không cần lấy product_id, sử dụng tên sản phẩm để xác định.
        Kiểm tra xem giỏ hàng có trống không"""
        if self.cart_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "Giỏ hàng đang trống.")
            return

        """ Lấy dòng được chọn trong bảng giỏ hàng"""
        selected_row = self.cart_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Vui lòng chọn một sản phẩm trong giỏ hàng.")
            return

        """ Lấy tên sản phẩm từ cột đầu tiên (cột tên sản phẩm)"""
        product_name_item = self.cart_table.item(selected_row, 0)
        if not product_name_item:
            QMessageBox.warning(self, "Error", "Không thể xác định sản phẩm được chọn.")
            return

        product_name = product_name_item.text()

        """ Tìm sản phẩm trong giỏ hàng dựa trên tên"""
        product_to_remove = None
        for item in self.cart.to_dict():
            product = self.productlist.get_product_by_id(item['product_id'])
            if product and product.name == product_name:
                product_to_remove = product
                break

        if not product_to_remove:
            QMessageBox.warning(self, "Error", "Không tìm thấy sản phẩm trong giỏ hàng.")
            return

        """ Xóa sản phẩm khỏi giỏ hàng"""
        self.cart.remove_product(product_to_remove.id)
        self.update_cart_table()
        QMessageBox.information(self, "Success", f"Sản phẩm '{product_name}' đã được xóa khỏi giỏ hàng.")

    def checkout(self):
        total, tax, total_after_tax = self.cart.checkout()

        if total == -1:
            QMessageBox.warning(self, "Error", "Giỏ hàng đang trống.")
        else:
            invoice = Invoice(self.cart.get_cart(), total,tax, total_after_tax)  # Tạo hóa đơn mới

            invoice.save_to_json()

            for item in self.cart.to_dict():
                success = self.productlist.reduce_stock(item['product_id'], item['qty'])
                if success is False:
                    QMessageBox.warning(self, "Lỗi", f"Sản phẩm {item['product_id']} không đủ hàng.")

            self.productlist.save_products()
            self.load_products()
            dialog = InvoiceDialog(invoice, self)
            dialog.exec()
            self.cart.clear()
            self.label_subtotal.setText(f" {invoice.total:,.0f}đ")
            self.label_tax.setText(f" {invoice.tax:,.0f}đ")
            self.label_total.setText(f" {invoice.total_after_tax:,.0f}đ")

            self.update_cart_table()

    def cancle(self):
        self.cart.clear()
        self.update_cart_table()


    def filter_product(self, category="Beverages"):
        """ Cập nhật danh mục hiện tại"""
        self.current_category = category

        if hasattr(self, "selected_frames"):
            self.selected_frames.clear()

        """ Lọc sản phẩm theo danh mục"""
        filtered_products = [p for p in self.productlist.products if p.category == category]

        """ Xóa widget cũ"""
        for i in reversed(range(self.product_container.count())):
            widget = self.product_container.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        """ Thêm sản phẩm vào layout theo hàng và cột"""
        row, col = 0, 0
        for product in filtered_products:
            self.add_product(product, row, col)
            col += 1
            if col >= 3:  # Hiển thị 3 sản phẩm trên một hàng
                col = 0
                row += 1

        self.scroll_widget.adjustSize()
        self.scroll_area.verticalScrollBar().setValue

"""Giao diện Login"""
class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.setWindowTitle("Đăng nhập")
        self.dinhnghianutlenh()

    """ liên kết nút lệnh"""
    def dinhnghianutlenh(self):
        self.pushButton_login.clicked.connect(self.login)

    def login(self):
        """Kiểm tra đăng nhập và mở cửa sổ Manager"""
        try:
            admin_list = AdminList()
            username = self.lineEdit_name.text().strip()
            password = self.lineEdit_password.text().strip()
            print(username, password)

            if admin_list.check_login(username, password):
                QMessageBox.information(self, "Success", "Đăng nhập thành công!")

                self.manager_window = ManagerWindow(username)  # Tạo cửa sổ Manager
                self.manager_window.show()
                self.hide()

            else:
                QMessageBox.warning(self, "Error", "Sai tài khoản hoặc mật khẩu!")

        except Exception as e:
            print(f"Đã xảy ra lỗi khi kiểm tra đăng nhập: {e}")

"""Giao diện Manager"""
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6 import uic
from CProductList import ProductList

class ManagerWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        uic.loadUi("manage.ui", self)
        self.setWindowTitle(f"Quản lý sản phẩm - {username}")
        self.dinhnghianutlenh()

        self.product_list = ProductList()
        self.load_products()
        self.username = username  # Lưu tên admin
        self.admin_name = admin_name

    """ liên kết nút lệnh"""
    def dinhnghianutlenh(self):
        self.pushButton_update.clicked.connect(self.update_stock)

    def load_products(self):
        """Tải danh sách sản phẩm vào bảng"""
        self.tableWidget.setRowCount(len(self.product_list.products))
        for row, product in enumerate(self.product_list.products):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(product.id))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(product.name))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(product.category))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(product.price)))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(product.stock)))

    def update_stock(self):
        """Cập nhật số lượng sản phẩm"""
        product_id = self.lineEdit_ID.text()
        quantity = self.lineEdit_SL.text()

        if not product_id or not quantity.isdigit():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mã sản phẩm và số lượng hợp lệ!")
            return
        success = self.product_list.update_product_stock(product_id, int(quantity), self.admin_name)
        if success:
            QMessageBox.information(self, "Thành công", "Cập nhật số lượng thành công!")
            self.load_products()
        else:
            QMessageBox.warning(self, "Lỗi", "Mã sản phẩm không tồn tại!")

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()

