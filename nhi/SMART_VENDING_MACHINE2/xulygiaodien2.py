import sys
import json
import os
import datetime
import uuid
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
                             QTabWidget, QFrame, QSpacerItem, QSizePolicy, QMessageBox,
                             QLineEdit)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon


class Product:
    def __init__(self, product_id, name, price, category, image_path, quantity_available=10, description=""):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.image_path = image_path
        self.quantity_available = quantity_available
        self.description = description

    def get_details(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "quantity_available": self.quantity_available,
            "description": self.description
        }

    def update_stock(self, quantity):
        if self.quantity_available >= quantity:
            self.quantity_available -= quantity
            return True
        return False

    def is_available(self):
        return self.quantity_available > 0


class Cart:
    def __init__(self, tax_rate=0.10):
        self.items = {}  # product_id: {"product": product_obj, "quantity": qty}
        self.total_amount = 0.0
        self.tax_rate = tax_rate
        self.tax_amount = 0.0

    def add_item(self, product, quantity=1):
        if product.product_id in self.items:
            self.items[product.product_id]["quantity"] += quantity
        else:
            self.items[product.product_id] = {"product": product, "quantity": quantity}
        self.calculate_total()
        return True

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            self.calculate_total()
            return True
        return False

    def update_quantity(self, product_id, quantity):
        if product_id in self.items:
            self.items[product_id]["quantity"] = quantity
            self.calculate_total()
            return True
        return False

    def calculate_total(self):
        self.total_amount = sum(item["product"].price * item["quantity"] for item in self.items.values())
        self.calculate_tax()
        return self.total_amount

    def calculate_tax(self):
        self.tax_amount = self.total_amount * self.tax_rate
        return self.tax_amount

    def get_final_total(self):
        return self.total_amount + self.tax_amount

    def clear_cart(self):
        self.items = {}
        self.total_amount = 0.0
        self.tax_amount = 0.0

    def get_cart_items(self):
        return self.items

    def generate_receipt(self, transaction_id, store_name):
        receipt = {
            "transaction_id": transaction_id,
            "store_name": store_name,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": [],
            "subtotal": self.total_amount,
            "tax_rate": f"{self.tax_rate * 100}%",
            "tax_amount": self.tax_amount,
            "total": self.get_final_total()
        }

        for product_id, item in self.items.items():
            receipt["items"].append({
                "name": item["product"].name,
                "price": item["product"].price,
                "quantity": item["quantity"],
                "subtotal": item["product"].price * item["quantity"]
            })

        return receipt


class VendingMachine:
    def __init__(self, store_name="Convenience Store"):
        self.products = {}
        self.categories = []
        self.cart = Cart()
        self.store_name = store_name
        self.transaction_counter = 0
        self.transaction_history = []

    def generate_transaction_id(self):
        self.transaction_counter += 1
        return f"TRX-{datetime.datetime.now().strftime('%Y%m%d')}-{self.transaction_counter:04d}"

    def load_products(self, products_data):
        for data in products_data:
            product = Product(
                product_id=data["product_id"],
                name=data["name"],
                price=data["price"],
                category=data["category"],
                image_path=data["image_path"],
                quantity_available=data.get("quantity_available", 10),
                description=data.get("description", "")
            )
            self.products[product.product_id] = product

            if product.category not in self.categories:
                self.categories.append(product.category)

    def get_products_by_category(self, category):
        return {pid: product for pid, product in self.products.items() if product.category == category}

    def search_products(self, keyword):
        keyword = keyword.lower()
        return {
            pid: product for pid, product in self.products.items()
            if keyword in product.name.lower() or keyword in product.description.lower()
        }

    def add_to_cart(self, product_id, quantity=1):
        if product_id in self.products and self.products[product_id].is_available():
            product = self.products[product_id]
            result = self.cart.add_item(product, quantity)
            return result
        return False

    def remove_from_cart(self, product_id):
        return self.cart.remove_item(product_id)

    def update_cart_quantity(self, product_id, quantity):
        return self.cart.update_quantity(product_id, quantity)

    def get_cart_total(self):
        return self.cart.get_final_total()

    def checkout(self):
        # First check if products are available in the required quantities
        for product_id, item in self.cart.items.items():
            product = item["product"]
            quantity = item["quantity"]
            if product.quantity_available < quantity:
                return False, f"Not enough stock for {product.name}. Only {product.quantity_available} available."

        # Process the transaction
        transaction_id = self.generate_transaction_id()
        receipt = self.cart.generate_receipt(transaction_id, self.store_name)

        # Update inventory
        for product_id, item in self.cart.items.items():
            product = item["product"]
            quantity = item["quantity"]
            product.update_stock(quantity)

        # Save transaction
        self.transaction_history.append(receipt)

        # Clear cart
        self.cart.clear_cart()

        return True, receipt

    def get_transaction_history(self):
        return self.transaction_history


class ProductCard(QFrame):
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product = product
        self.setup_ui()

    def setup_ui(self):
        self.setFrameShape(QFrame.Shape.Box)
        self.setStyleSheet("QFrame { border: 1px solid #ccc; border-radius: 5px; background-color: white; }")
        self.setFixedSize(150, 180)

        layout = QVBoxLayout(self)

        # Product image
        image_label = QLabel()
        try:
            pixmap = QPixmap(self.product.image_path)
            pixmap = pixmap.scaled(120, 100, Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        except:
            image_label.setText("No Image")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Product name
        name_label = QLabel(self.product.name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        font = QFont()
        font.setBold(True)
        name_label.setFont(font)

        # Product price
        price_label = QLabel(f"${self.product.price:.2f}")
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add to cart button
        add_button = QPushButton("Add to Cart")
        add_button.setStyleSheet("background-color: #4CAF50; color: white;")
        add_button.clicked.connect(self.add_to_cart)

        layout.addWidget(image_label)
        layout.addWidget(name_label)
        layout.addWidget(price_label)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_to_cart(self):
        # This will be connected to the main window's add_to_cart method
        main_window = self.window()
        if hasattr(main_window, 'add_to_cart'):
            main_window.add_to_cart(self.product)


class CartItemWidget(QWidget):
    def __init__(self, product, quantity, parent=None):
        super().__init__(parent)
        self.product = product
        self.quantity = quantity
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)

        # Product name and price
        info_layout = QVBoxLayout()
        name_label = QLabel(self.product.name)
        font = QFont()
        font.setBold(True)
        name_label.setFont(font)

        price_label = QLabel(f"${self.product.price:.2f}")

        info_layout.addWidget(name_label)
        info_layout.addWidget(price_label)

        # Quantity
        quantity_label = QLabel(f"{self.quantity}")
        quantity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtotal
        subtotal_label = QLabel(f"${self.product.price * self.quantity:.2f}")
        subtotal_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Remove button
        remove_button = QPushButton("×")
        remove_button.setFixedSize(30, 30)
        remove_button.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; border-radius: 15px;")
        remove_button.clicked.connect(self.remove_from_cart)

        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(quantity_label)
        layout.addStretch()
        layout.addWidget(subtotal_label)
        layout.addWidget(remove_button)

        self.setLayout(layout)

    def remove_from_cart(self):
        main_window = self.window()
        if hasattr(main_window, 'remove_from_cart'):
            main_window.remove_from_cart(self.product.product_id)


class VendingMachineApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.vending_machine = VendingMachine("Convenience Store")
        self.load_sample_data()
        self.setup_ui()

    def load_sample_data(self):
        # Load sample product data
        sample_data = [
            {
                "product_id": "snk001",
                "name": "Potato Chips",
                "price": 2.99,
                "category": "Snacks",
                "image_path": "img/chips.png",
                "quantity_available": 20,
                "description": "Crispy potato chips"
            },
            {
                "product_id": "snk002",
                "name": "Chocolate Bar",
                "price": 1.99,
                "category": "Snacks",
                "image_path": "img/chocolate.png",
                "quantity_available": 30,
                "description": "Sweet milk chocolate"
            },
            {
                "product_id": "bvg001",
                "name": "Water Bottle",
                "price": 1.49,
                "category": "Beverages",
                "image_path": "img/water.png",
                "quantity_available": 40,
                "description": "Refreshing spring water"
            },
            {
                "product_id": "bvg002",
                "name": "Cola",
                "price": 2.49,
                "category": "Beverages",
                "image_path": "img/cola.png",
                "quantity_available": 25,
                "description": "Carbonated cola drink"
            },
            {
                "product_id": "per001",
                "name": "Toothbrush",
                "price": 3.99,
                "category": "Personal Items",
                "image_path": "img/toothbrush.png",
                "quantity_available": 15,
                "description": "Soft bristle toothbrush"
            },
            {
                "product_id": "per002",
                "name": "Tissue Pack",
                "price": 1.29,
                "category": "Personal Items",
                "image_path": "img/tissue.png",
                "quantity_available": 35,
                "description": "Soft facial tissues"
            }
        ]

        self.vending_machine.load_products(sample_data)

    def setup_ui(self):
        self.setWindowTitle("Self-Service Vending Machine")
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Left section (Products)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_products)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        left_layout.addLayout(search_layout)

        # Products tabs
        self.tab_widget = QTabWidget()
        self.create_product_tabs()

        left_layout.addWidget(self.tab_widget)

        # Right section (Cart)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        cart_label = QLabel("Your Cart")
        cart_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))

        self.cart_widget = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_widget)

        # Cart items scroll area
        cart_scroll = QScrollArea()
        cart_scroll.setWidgetResizable(True)
        cart_scroll.setWidget(self.cart_widget)

        # Total section
        total_widget = QWidget()
        total_layout = QVBoxLayout(total_widget)

        # Subtotal
        subtotal_layout = QHBoxLayout()
        subtotal_label = QLabel("Subtotal:")
        self.subtotal_value = QLabel("$0.00")
        self.subtotal_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        subtotal_layout.addWidget(subtotal_label)
        subtotal_layout.addWidget(self.subtotal_value)

        # Tax
        tax_layout = QHBoxLayout()
        tax_label = QLabel("Tax (10%):")
        self.tax_value = QLabel("$0.00")
        self.tax_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        tax_layout.addWidget(tax_label)
        tax_layout.addWidget(self.tax_value)

        # Total
        total_layout_row = QHBoxLayout()
        total_label = QLabel("Total:")
        total_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.total_value = QLabel("$0.00")
        self.total_value.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.total_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        total_layout_row.addWidget(total_label)
        total_layout_row.addWidget(self.total_value)

        # Add to total layout
        total_layout.addLayout(subtotal_layout)
        total_layout.addLayout(tax_layout)
        total_layout.addLayout(total_layout_row)

        # Checkout button
        pay_button = QPushButton("Pay")
        pay_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; height: 40px;")
        pay_button.clicked.connect(self.checkout)

        # Add to right layout
        right_layout.addWidget(cart_label)
        right_layout.addWidget(cart_scroll)
        right_layout.addWidget(total_widget)
        right_layout.addWidget(pay_button)

        # Set sizes for left and right sections
        main_layout.addWidget(left_widget, 3)
        main_layout.addWidget(right_widget, 2)

        self.setCentralWidget(central_widget)

        # Update cart display
        self.update_cart_display()

    def create_product_tabs(self):
        # Create "All Products" tab
        all_products_widget = QWidget()
        all_layout = QGridLayout(all_products_widget)

        row, col = 0, 0
        max_cols = 4

        for product_id, product in self.vending_machine.products.items():
            product_card = ProductCard(product)
            all_layout.addWidget(product_card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        self.tab_widget.addTab(all_products_widget, "All Products")

        # Create tab for each category
        for category in self.vending_machine.categories:
            category_widget = QWidget()
            category_layout = QGridLayout(category_widget)

            row, col = 0, 0

            category_products = self.vending_machine.get_products_by_category(category)
            for product_id, product in category_products.items():
                product_card = ProductCard(product)
                category_layout.addWidget(product_card, row, col)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

            self.tab_widget.addTab(category_widget, category)

    def search_products(self):
        keyword = self.search_input.text()
        if not keyword:
            return

        search_results = self.vending_machine.search_products(keyword)

        # Create search results tab
        search_widget = QWidget()
        search_layout = QGridLayout(search_widget)

        row, col = 0, 0
        max_cols = 4

        for product_id, product in search_results.items():
            product_card = ProductCard(product)
            search_layout.addWidget(product_card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # If there's already a search tab, remove it
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Search Results":
                self.tab_widget.removeTab(i)
                break

        # Add the new search tab and switch to it
        self.tab_widget.addTab(search_widget, "Search Results")
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)

    def add_to_cart(self, product):
        if self.vending_machine.add_to_cart(product.product_id):
            self.update_cart_display()

    def remove_from_cart(self, product_id):
        if self.vending_machine.remove_from_cart(product_id):
            self.update_cart_display()

    def update_cart_display(self):
        # Clear current cart widgets
        for i in reversed(range(self.cart_layout.count())):
            widget = self.cart_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add cart items
        cart_items = self.vending_machine.cart.get_cart_items()
        for product_id, item in cart_items.items():
            product = item["product"]
            quantity = item["quantity"]
            cart_item_widget = CartItemWidget(product, quantity)
            self.cart_layout.addWidget(cart_item_widget)

        # Add spacer if cart is not empty
        if cart_items:
            spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.cart_layout.addItem(spacer)

        # Update totals
        subtotal = self.vending_machine.cart.total_amount
        tax = self.vending_machine.cart.tax_amount
        total = self.vending_machine.cart.get_final_total()

        self.subtotal_value.setText(f"${subtotal:.2f}")
        self.tax_value.setText(f"${tax:.2f}")
        self.total_value.setText(f"${total:.2f}")

    def checkout(self):
        cart_items = self.vending_machine.cart.get_cart_items()
        if not cart_items:
            QMessageBox.warning(self, "Empty Cart", "Your cart is empty. Please add items before checkout.")
            return

        success, result = self.vending_machine.checkout()

        if success:
            self.show_receipt(result)
            self.update_cart_display()
        else:
            QMessageBox.warning(self, "Checkout Failed", result)

    def show_receipt(self, receipt):
        receipt_text = f"===== RECEIPT =====\n"
        receipt_text += f"Store: {receipt['store_name']}\n"
        receipt_text += f"Transaction ID: {receipt['transaction_id']}\n"
        receipt_text += f"Date: {receipt['date']}\n"
        receipt_text += f"-------------------\n"

        for item in receipt['items']:
            receipt_text += f"{item['name']} x {item['quantity']}: ${item['subtotal']:.2f}\n"

        receipt_text += f"-------------------\n"
        receipt_text += f"Subtotal: ${receipt['subtotal']:.2f}\n"
        receipt_text += f"Tax ({receipt['tax_rate']}): ${receipt['tax_amount']:.2f}\n"
        receipt_text += f"Total: ${receipt['total']:.2f}\n"
        receipt_text += f"===================\n"
        receipt_text += f"Thank you for your purchase!"

        receipt_dialog = QMessageBox()
        receipt_dialog.setWindowTitle("Receipt")
        receipt_dialog.setText(receipt_text)
        receipt_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        receipt_dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VendingMachineApp()
    window.show()
    sys.exit(app.exec())