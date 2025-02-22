# menu.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from models import Item

class MenuWindow(QWidget):
    def __init__(self, cart, update_cart_display_callback):
        super().__init__()
        self.cart = cart
        self.update_cart_display = update_cart_display_callback
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Menu")
        self.setGeometry(200, 200, 300, 400)

        layout = QVBoxLayout()

        # Predefined products
        products = [
            ("Water", 1.00),
            ("Instant Noodle", 2.50),
            ("Bread", 3.00),
            ("Juice", 2.00),
            ("Milk", 2.80)
        ]

        for name, price in products:
            btn = QPushButton(f"{name} - ${price:.2f}")
            btn.clicked.connect(lambda checked, n=name, p=price: self.add_to_cart(n, p))
            layout.addWidget(btn)

        self.setLayout(layout)

    def add_to_cart(self, name, price):
        item = Item(name, price)
        self.cart.add_item(item, 1)
        self.update_cart_display()
