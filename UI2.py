import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox, QGridLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity=1):
        # Check if the item already exists in the cart
        for i, (cart_item, qty) in enumerate(self.items):
            if cart_item.name == item.name:
                self.items[i] = (cart_item, qty + quantity)
                return
        self.items.append((item, quantity))

    def remove_item(self, item_name):
        self.items = [item for item in self.items if item[0].name != item_name]

    def calculate_total(self):
        return sum(item.price * quantity for item, quantity in self.items)

    def display_cart(self):
        cart_details = "\nItems in Cart:\n"
        for item, quantity in self.items:
            cart_details += f"{item.name}: {quantity} x ${item.price:.2f} = ${item.price * quantity:.2f}\n"
        cart_details += f"Total: ${self.calculate_total():.2f}"
        return cart_details

class POSSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cart = Cart()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("POS System")
        self.setGeometry(100, 100, 800, 600)

        # Set background color
        self.setStyleSheet("background-color: #f0f0f0;")

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Title label
        title_label = QLabel("POS System")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title_label)

        # Menu and Cart layout
        menu_cart_layout = QHBoxLayout()

        # Menu section
        menu_widget = QWidget()
        menu_layout = QGridLayout()
        menu_widget.setLayout(menu_layout)

        # Predefined products
        self.products = [
            Item("Water", 1.00),
            Item("Snack", 2.50),
            Item("Instant Noodle", 3.00),
            Item("Soda", 1.50),
            Item("Chips", 2.00),
        ]

        # Add product buttons to the menu
        for i, product in enumerate(self.products):
            button = QPushButton(f"{product.name}\n${product.price:.2f}")
            button.setStyleSheet("background-color: #27ae60; color: white; font-size: 14px; padding: 10px;")
            button.clicked.connect(lambda _, p=product: self.add_item_to_cart(p))
            menu_layout.addWidget(button, i // 2, i % 2)

        menu_cart_layout.addWidget(menu_widget)

        # Cart display section
        cart_widget = QWidget()
        cart_layout = QVBoxLayout()
        cart_widget.setLayout(cart_layout)

        self.cart_display = QTextEdit()
        self.cart_display.setReadOnly(True)
        self.cart_display.setStyleSheet("background-color: #ffffff; color: #34495e; font-size: 14px;")
        cart_layout.addWidget(self.cart_display)

        # Remove buttons for items in the cart
        self.remove_buttons = {}
        for product in self.products:
            button = QPushButton(f"Remove {product.name}")
            button.setStyleSheet("background-color: #e74c3c; color: white; font-size: 14px; padding: 10px;")
            button.clicked.connect(lambda _, p=product: self.remove_item_from_cart(p))
            button.hide()  # Hide by default
            cart_layout.addWidget(button)
            self.remove_buttons[product.name] = button

        menu_cart_layout.addWidget(cart_widget)
        layout.addLayout(menu_cart_layout)

        # Process Payment and Exit buttons
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
        self.remove_buttons[product.name].show()  # Show the remove button for this product

    def remove_item_from_cart(self, product):
        self.cart.remove_item(product.name)
        self.update_cart_display()
        self.remove_buttons[product.name].hide()  # Hide the remove button if the item is removed

    def process_payment(self):
        cart_details = self.cart.display_cart()
        # Create a custom dialog for payment method selection
        payment_dialog = QMessageBox(self)
        payment_dialog.setWindowTitle("Process Payment")
        payment_dialog.setText(f"{cart_details}\n\nSelect payment method:")

        # Add custom buttons for cash and credit
        cash_button = payment_dialog.addButton("Cash", QMessageBox.ButtonRole.YesRole)
        credit_button = payment_dialog.addButton("Credit", QMessageBox.ButtonRole.NoRole)
        cancel_button = payment_dialog.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        # Show the dialog and wait for user input
        payment_dialog.exec()

        # Determine which button was clicked
        clicked_button = payment_dialog.clickedButton()
        if clicked_button == cash_button:
            payment_method = "cash"
        elif clicked_button == credit_button:
            payment_method = "credit"
        else:
            return  # User clicked Cancel, do nothing

        # Process the payment
        total_amount = self.cart.calculate_total()
        QMessageBox.information(self, "Payment Processed",
                                f"Payment of ${total_amount:.2f} made using {payment_method}. Thank you for your purchase!")
        self.cart = Cart()
        self.update_cart_display()
        for button in self.remove_buttons.values():
            button.hide()  # Hide all remove buttons after payment

    def update_cart_display(self):
        self.cart_display.setText(self.cart.display_cart())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pos_system = POSSystem()
    pos_system.show()
    sys.exit(app.exec())