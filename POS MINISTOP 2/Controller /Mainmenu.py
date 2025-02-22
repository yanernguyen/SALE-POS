import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox, QGridLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class POSSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cart = Cart()
        self.products = self.load_products_from_json()
        self.initUI()

    def load_products_from_json(self):
        """Loads product data from a JSON file."""
        try:
            with open("products.json", "r") as file:
                product_data = json.load(file)
                return [Item(p["name"], p["price"]) for p in product_data]
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "products.json not found! Using default products.")
            return []

    def save_products_to_json(self):
        """Saves updated product data to a JSON file."""
        product_data = [{"name": item.name, "price": item.price} for item in self.products]
        with open("products.json", "w") as file:
            json.dump(product_data, file, indent=4)

    def initUI(self):
        self.setWindowTitle("POS System")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        title_label = QLabel("POS System")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title_label)

        menu_cart_layout = QHBoxLayout()

        menu_widget = QWidget()
        menu_layout = QGridLayout()
        menu_widget.setLayout(menu_layout)

        # Add product buttons dynamically from JSON
        self.remove_buttons = {}  # Store remove buttons for later use
        for i, product in enumerate(self.products):
            button = QPushButton(f"{product.name}\n${product.price:.2f}")
            button.setStyleSheet("background-color: #27ae60; color: white; font-size: 14px; padding: 10px;")
            button.clicked.connect(lambda _, p=product: self.add_item_to_cart(p))
            menu_layout.addWidget(button, i // 2, i % 2)

        menu_cart_layout.addWidget(menu_widget)

        cart_widget = QWidget()
        cart_layout = QVBoxLayout()
        cart_widget.setLayout(cart_layout)

        self.cart_display = QTextEdit()
        self.cart_display.setReadOnly(True)
        self.cart_display.setStyleSheet("background-color: #ffffff; color: #34495e; font-size: 14px;")
        cart_layout.addWidget(self.cart_display)

        # Create remove buttons dynamically
        for product in self.products:
            button = QPushButton(f"Remove {product.name}")
            button.setStyleSheet("background-color: #e74c3c; color: white; font-size: 14px; padding: 10px;")
            button.clicked.connect(lambda _, p=product: self.remove_item_from_cart(p))
            button.hide()
            cart_layout.addWidget(button)
            self.remove_buttons[product.name] = button

        menu_cart_layout.addWidget(cart_widget)
        layout.addLayout(menu_cart_layout)

        buttons_layout = QHBoxLayout()

        process_payment_button = QPushButton("Process Payment")
        process_payment_button.setStyleSheet("background-color: #3498db; color: white; font-size: 14px; padding: 10px;")
        process_payment_button.clicked.connect(self.process_payment)
        buttons_layout.addWidget(process_payment_button)

        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("background-color: #95a5a6; color: white; font-size: 14px; padding: 10px;")
        exit_button.clicked.connect(self.close)
        buttons_layout.addWidget(exit_button)

        layout.addLayout(buttons_layout)
        main_widget.setLayout(layout)

    def add_item_to_cart(self, product):
        self.cart.add_item(product)
        self.update_cart_display()
        self.remove_buttons[product.name].show()  # Show the remove button

    def remove_item_from_cart(self, product):
        self.cart.remove_item(product.name)
        self.update_cart_display()
        self.remove_buttons[product.name].hide()  # Hide the button when item is removed

    def process_payment(self):
        cart_details = self.cart.display_cart()
        payment_dialog = QMessageBox(self)
        payment_dialog.setWindowTitle("Process Payment")
        payment_dialog.setText(f"{cart_details}\n\nSelect payment method:")

        cash_button = payment_dialog.addButton("Cash", QMessageBox.ButtonRole.YesRole)
        credit_button = payment_dialog.addButton("Credit", QMessageBox.ButtonRole.NoRole)
        cancel_button = payment_dialog.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        payment_dialog.exec()
        clicked_button = payment_dialog.clickedButton()
        if clicked_button == cash_button:
            payment_method = "cash"
        elif clicked_button == credit_button:
            payment_method = "credit"
        else:
            return

        total_amount = self.cart.calculate_total()
        QMessageBox.information(self, "Payment Processed",
                                f"Payment of ${total_amount:.2f} made using {payment_method}. Thank you for your purchase!")
        self.cart = Cart()
        self.update_cart_display()
        for button in self.remove_buttons.values():
            button.hide()

    def update_cart_display(self):
        self.cart_display.setText(self.cart.display_cart())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pos_system = POSSystem()
    pos_system.show()
    sys.exit(app.exec())
