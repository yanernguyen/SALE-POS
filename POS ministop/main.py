import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QScrollArea,
    QInputDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from models import Cart
from menu import MenuWindow


class POSSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cart = Cart()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("POS System")
        self.setGeometry(100, 100, 600, 400)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Title label
        title_label = QLabel("POS System")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title_label)

        # Scrollable Cart Display
        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_container = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_container)
        self.cart_scroll.setWidget(self.cart_container)
        layout.addWidget(self.cart_scroll)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Open Menu button
        open_menu_button = QPushButton("Open Menu")
        open_menu_button.setStyleSheet("background-color: #f39c12; color: white; font-size: 14px; padding: 10px;")
        open_menu_button.clicked.connect(self.open_menu)
        buttons_layout.addWidget(open_menu_button)

        # Process Payment button
        process_payment_button = QPushButton("Process Payment")
        process_payment_button.setStyleSheet("background-color: #3498db; color: white; font-size: 14px; padding: 10px;")
        process_payment_button.clicked.connect(self.process_payment)
        buttons_layout.addWidget(process_payment_button)

        # Exit button
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("background-color: #95a5a6; color: white; font-size: 14px; padding: 10px;")
        exit_button.clicked.connect(self.close)
        buttons_layout.addWidget(exit_button)

        layout.addLayout(buttons_layout)
        main_widget.setLayout(layout)

        self.update_cart_display()

    def open_menu(self):
        """ Opens the product menu. """
        self.menu_window = MenuWindow(self.cart, self.update_cart_display)
        self.menu_window.show()

    def update_cart_display(self):
        """ Updates the cart display with clickable buttons for each item. """
        # Clear existing buttons
        for i in reversed(range(self.cart_layout.count())):
            widget = self.cart_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add buttons for each cart item
        for item, quantity in self.cart.items:
            item_button = QPushButton(f"{item.name} ({quantity}x) - ${item.price * quantity:.2f}")
            item_button.setStyleSheet("background-color: #e74c3c; color: white; font-size: 14px; padding: 5px;")
            item_button.clicked.connect(lambda checked, n=item.name, q=quantity: self.remove_item_from_cart(n, q))
            self.cart_layout.addWidget(item_button)

    def remove_item_from_cart(self, item_name, current_quantity):
        """ Allows user to select how many units to remove. """
        remove_quantity, ok = QInputDialog.getInt(self, "Remove Item",
                                                  f"Enter quantity to remove (1-{current_quantity}):", 1, 1,
                                                  current_quantity)

        if ok:
            self.cart.remove_item(item_name, remove_quantity)
            self.update_cart_display()
            QMessageBox.information(self, "Item Removed", f"Removed {remove_quantity} x {item_name} from cart.")

    def process_payment(self):
        """ Processes the payment and resets the cart. """
        total_amount = self.cart.calculate_total()
        QMessageBox.information(self, "Payment Processed", f"Payment of ${total_amount:.2f} completed. Thank you!")
        self.cart = Cart()
        self.update_cart_display()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pos_system = POSSystem()
    pos_system.show()
    sys.exit(app.exec())
