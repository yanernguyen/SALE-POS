import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit,
    QMessageBox, QInputDialog
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity):
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
        self.setGeometry(100, 100, 600, 400)

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

        # Cart display
        self.cart_display = QTextEdit()
        self.cart_display.setReadOnly(True)
        self.cart_display.setStyleSheet("background-color: #ffffff; color: #34495e; font-size: 14px;")
        layout.addWidget(self.cart_display)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Add Item button
        add_item_button = QPushButton("Add Item")
        add_item_button.setStyleSheet("background-color: #27ae60; color: white; font-size: 14px; padding: 10px;")
        add_item_button.clicked.connect(self.add_item_to_cart)
        buttons_layout.addWidget(add_item_button)

        # Remove Item button
        remove_item_button = QPushButton("Remove Item")
        remove_item_button.setStyleSheet("background-color: #e74c3c; color: white; font-size: 14px; padding: 10px;")
        remove_item_button.clicked.connect(self.remove_item_from_cart)
        buttons_layout.addWidget(remove_item_button)

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

    def add_item_to_cart(self):
        name, ok1 = QInputDialog.getText(self, "Add Item", "Enter item name:")
        if ok1:
            price, ok2 = QInputDialog.getDouble(self, "Add Item", f"Enter price of {name}:", min=0.01)
            if ok2:
                quantity, ok3 = QInputDialog.getInt(self, "Add Item", f"Enter quantity of {name}:", min=1)
                if ok3:
                    item = Item(name, price)
                    self.cart.add_item(item, quantity)
                    self.update_cart_display()
                    QMessageBox.information(self, "Item Added", f"Added {quantity} x {name} to cart.")

    def remove_item_from_cart(self):
        item_name, ok = QInputDialog.getText(self, "Remove Item", "Enter item name to remove:")
        if ok:
            self.cart.remove_item(item_name)
            self.update_cart_display()
            QMessageBox.information(self, "Item Removed", f"Removed {item_name} from cart.")

    def process_payment(self):
        cart_details = self.cart.display_cart()
        payment_method, ok = QInputDialog.getItem(self, "Process Payment", "Select payment method:", ["cash", "credit"], 0, False)
        if ok:
            total_amount = self.cart.calculate_total()
            QMessageBox.information(self, "Payment Processed", f"Payment of ${total_amount:.2f} made using {payment_method}. Thank you for your purchase!")
            self.cart = Cart()
            self.update_cart_display()

    def update_cart_display(self):
        self.cart_display.setText(self.cart.display_cart())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pos_system = POSSystem()
    pos_system.show()
    sys.exit(app.exec())